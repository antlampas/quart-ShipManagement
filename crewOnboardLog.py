from quart          import Blueprint,current_app
from sqlalchemy     import select
from sqlalchemy.orm import Session

from model import db,CrewMemberTable,MemberDutyLogEntryTable,MemberOnboardLogEntryTable,MemberRankLogEntryTable,MemberDivisionLogEntryTable,MemberTaskLogEntryTable,MemberMissionLogEntryTable

crewOnboardLog_blueprint = Blueprint("crewOnboardLog",__name__,url_prefix='/crewOnboardLog',template_folder='templates/default')

class MemberOnboardLog:
    def __init__(self):
        self.CrewMember        = ""
        self.OnboardPeriods    = list()
        self.PreviousDivisions = list()
        self.PreviousDuties    = list()
        self.PreviousTasks     = list()
        self.PreviousMissions  = list()
    def read(self):
        log = list()

        with db.bind.Session() as s:
            with s.begin():
                crewMembers       = s.query(select(CrewMemberTable).distinct(CrewMemberTable.Nickname).subquery()).all()
                memberOnboardLog  = s.query(select(MemberOnboardLogEntryTable,CrewMemberTable).subquery()).all()
                memberDivisionLog = s.query(select(MemberDivisionLogEntryTable,CrewMemberTable).subquery()).all()
                memberDutyLog     = s.query(select(MemberDutyLogEntryTable,CrewMemberTable).subquery()).all()
                memberTaskLog     = s.query(select(MemberTaskLogEntryTable,CrewMemberTable).subquery()).all()
                memberMissionLog  = s.query(select(MemberMissionLogEntryTable,CrewMemberTable).subquery()).all()

                for i in (crewMembers,memberOnboardLog,memberDivisionLog,memberDutyLog,memberTaskLog,memberMissionLog):
                    if len(i) > 0:
                        log.append(i)

        return log

class OnboardLog:
    def __init__(self):
        self.logEntry = list()
    def read(self):
        log = list()

        with db.bind.Session() as s:
            with s.begin():
                crewMembers       = s.query(select(CrewMemberTable).distinct(CrewMemberTable.Nickname).where(CrewMemberTable.Nickname==member).subquery()).all()
                memberOnboardLog  = s.query(select(MemberOnboardLogEntryTable,CrewMemberTable).where(MemberOnboardLogEntryTable.CrewMember==member,MemberOnboardLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberDivisionLog = s.query(select(MemberDivisionLogEntryTable,CrewMemberTable).where(MemberDivisionLogEntryTable.CrewMember==member,MemberDivisionLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberDutyLog     = s.query(select(MemberDutyLogEntryTable,CrewMemberTable).where(MemberDutyLogEntryTable.CrewMember==member,MemberDutyLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberTaskLog     = s.query(select(MemberTaskLogEntryTable,CrewMemberTable).where(MemberTaskLogEntryTable.CrewMember==member,MemberTaskLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()
                memberMissionLog  = s.query(select(MemberMissionLogEntryTable,CrewMemberTable).where(MemberMissionLogEntryTable.CrewMember==member,MemberMissionLogEntryTable.CrewMember==CrewMemberTable.Nickname).subquery()).all()

                for i in (crewMembers,memberOnboardLog,memberDivisionLog,memberDutyLog,memberTaskLog,memberMissionLog):
                    if len(i) > 0:
                        log.append(i)

        return log

@crewOnboardLog_blueprint.route("/",methods=["GET"])
async def readLog():
    onboardLog = MemberOnboardLog()
    return render_template("crewOnboardLog.html",log=onboardLog.read())

@crewOnboardLog_blueprint.route("/<member>",methods=["GET"])
async def readMemberLog(member):
    onboardLog = OnboardLog()
    return render_template("crewOnboardLog.html",log=onboardLog.read())
