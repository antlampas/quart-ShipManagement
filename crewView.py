#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

import re
import requests
import json

from types          import SimpleNamespace
from time           import sleep
from jose           import jwt

from sqlalchemy     import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from quart          import Blueprint
from quart          import current_app
from quart          import request
from quart          import redirect
from quart          import url_for
from quart          import session

from config         import KeycloakConfig

from model          import db
from model          import loadFromDB
from model          import saveToDB

from forms          import AddCrewMemberForm
from forms          import RemoveCrewMemberForm
from forms          import EditCrewMemberForm

from authorization  import require_user
from authorization  import require_role
from authorization  import require_login
from authorization  import refreshToken

from permissions    import CrewPermissions

from crewClasses    import CrewMember
from crewClasses    import Crew

from standardReturn import standardReturn

crew_blueprint = Blueprint("crew",__name__,url_prefix='/crew',template_folder='templates/default')
sectionName    = "Crew"

@require_login
@refreshToken
@crew_blueprint.route("/",methods=["GET"])
async def crew():
    crewDB = loadFromDB('crew')
    if crewDB:
        return await standardReturn("crew.html",sectionName,CREW=crewList.Crew)
    else:
        return await standardReturn("error.html",sectionName,ERROR="No crew member found")

@require_user(groups=['Equipaggio'])
@refreshToken
@crew_blueprint.route("/member/<member>",methods=["GET"])
async def member(member):
    crewMember = loadFromDB('crew',member)
    if crewList:
        for cm in crewList.Crew:
            if cm.Nickname == member:
                crewMember = cm
                break
    if crewMember:
        return await standardReturn("crewMember.html",sectionName,CREWMEMBER=crewMember)
    else:
        return await standardReturn("error.html",sectionName,ERROR="Crew member not found")

@require_role(CrewPermissions.addMemberRole)
@refreshToken
@crew_blueprint.route("/add",methods=["GET","POST"])
async def add():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack too, make db managenet code
    #      more clear and check
    sectionName = 'Add ' + sectionName
    form   = AddCrewMemberForm()
    if request.method == 'GET':
        ranks     = []
        duties    = []
        divisions = []
        try:
            with db.bind.Session() as s:
                with s.begin():
                    ranks     = s.scalars(selectRank()).all()
                    duties    = s.scalars(selectDuty()).all()
                    divisions = s.scalars(selectDivision()).all()
        except Exception as e:
                return await standardReturn("error.html",sectionName,ERROR=str(e))
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        return await standardReturn("crewMemberAdd.html",sectionName,FORM=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            crewMember = CrewMember(FirstName = (await request.form)['FirstName'],
                                    LastName  = (await request.form)['LastName'],
                                    Nickname  = (await request.form)['Nickname'],
                                    Rank      = (await request.form)['Rank'],
                                    Division  = (await request.form)['Division'],
                                    Duties    = (await request.form)\
                                                                  .getlist('Duties')
                               )
            # form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
            # form.Duties.choices   = [(d.Name,d.Name) for d in duties]
            # form.Division.choices = [(d.Name,d.Name) for d in divisions]
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        saveToDB('crewMember',crewMember.__dict__)
            except Exception as e:
                    return await standardReturn("error.html",sectionName,ERROR="2: "+str(e))
            return await standardReturn("crewMemberAdd.html",
                                         sectionName,
                                         FORM=form,
                                         DUTIES=duties,
                                         MESSAGE='Success')
    else:
        return await standardReturn("error.html",sectionName,ERROR="Invalid method")

@require_role(CrewPermissions.removeMemberRole)
@refreshToken
@crew_blueprint.route("/remove",methods=["GET","POST"])
async def remove():
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack too, make db managenet code
    #      more clear and check
    sectionName = 'Remove ' + sectionName
    form = RemoveCrewMemberForm()
    crew = list()
    if request.method == 'GET':
        try:
            with db.bind.Session() as s:
                with s.begin():
                    crew = s.scalars(selectCrew()).all()
        except Exception as e:
            return await standardReturn("error.html",sectionName,ERROR="GET: "+str(e))
        form.Nickname.choices = [(c.Nickname,c.Nickname) for c in crew]
        return await standardReturn("crewMemberRemove.html",sectionName,FORM=form)
    elif request.method == 'POST':
        members = (await request.form).getlist('Nickname')
        if form.validate_on_submit():
            #TODO: move this to the "database management" code
            try:
                with db.bind.Session() as s:
                    with s.begin():
                        for member in members:
                            personId     = (s.scalar(selectPerson(attribute='nickname',search=member))).Id
                            memberSerial = (s.execute(selectCrew(member)).first())[3]
                            s.query(CrewMemberDivisionTable).filter_by(MemberSerial=memberSerial).delete()
                            s.query(CrewMemberDutyTable).filter_by(MemberSerial=memberSerial).delete()
                            s.query(CrewMemberRankTable).filter_by(MemberSerial=memberSerial).delete()
                            s.query(CrewMemberTable).filter_by(PersonalBaseInformationsId=personId).delete()
                            s.query(PersonalBaseInformationsTable).filter_by(Nickname=member).delete()
                        s.commit()
                        s.flush()
            except Exception as e:
                return await standardReturn("error.html",sectionName,ERROR="1: "+str(e))
            #TODO: End move
        return redirect(url_for('crew.remove'))
    else:
        return await standardReturn("error.html",sectionName,ERROR="Invalid method")


@require_role(CrewPermissions.editMemberRole)
@refreshToken
@crew_blueprint.route("/edit/",methods=["GET","POST"])
async def edit():
    sectionName = 'Edit ' + sectionName
    return await standardReturn("error.html",sectionName,ERROR='No member specified')

@require_role(CrewPermissions.editMemberRole)
@refreshToken
@crew_blueprint.route("/edit/<member>",methods=["GET","POST"])
async def editMember(member):
    return await standardReturn("implement.html",sectionName,implement="Implement!")
    #TODO: Make it work with keycloack too, make db managenet code
    #      more clear and check
    sectionName = 'Edit ' + sectionName
    form         = EditCrewMemberForm()
    ranks        = []
    duties       = []
    divisions    = []
    crewMember   = None
    crew         = None
    if request.method == 'GET':
        try:
            crewMember = CrewMember(Nickname=member)
        except Exception as e:
            return await standardReturn("error.html",sectionName,ERROR="GET: "+str(e))

        member = CrewMember(FirstName = personalBaseInformations.FirstName,
                            LastName  = personalBaseInformations.LastName,
                            Nickname  = personalBaseInformations.Nickname,
                            Rank      = crewMemberRank.RankName,
                            Division  = crewMemberDivision.DivisionName,
                            Duties    = [ d.DutyName for d in crewMemberDuties ]
                           )
        form.FirstName.data   = member.FirstName
        form.LastName.data    = member.LastName
        form.Rank.choices     = [(r.Name,r.Name) for r in ranks]
        form.Rank.default     = member.RankName
        form.Division.choices = [(d.Name,d.Name) for d in divisions]
        form.Division.default = member.DivisionName
        form.Duties.choices   = [(d.Name,d.Name) for d in duties]
        form.Duties.default   = [(d.DutyName,d.DutyName) for d in member.Duties]
        return await standardReturn("crewMemberEdit.html",sectionName,FORM=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            firstname      = (await request.form)['FirstName']
            lastname       = (await request.form)['LastName']
            nickname       = (await request.form)['Nickname']
            rank           = (await request.form)['Rank']
            division       = (await request.form)['Division']
            selectedDuties = (await request.form).getlist('Duties')

            member = CrewMember(FirstName = firstname,
                                LastName  = lastname,
                                Nickname  = nickname,
                                Rank      = rank,
                                Division  = division,
                                Duties    = selectedDuties
                               )
            saveToDB('crewMemberEdit',member.__dict__)
            return redirect(url_for('crew.edit',member=personalBaseInformations.Nickname))
    else:
        return await standardReturn("error.html",sectionName,ERROR="Invalid method")
