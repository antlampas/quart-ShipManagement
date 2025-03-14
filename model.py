from config                     import Config
from sqlalchemy.orm             import Mapped, mapped_column,DeclarativeBase,relationship
from sqlalchemy                 import ForeignKey,select
from quart_sqlalchemy           import SQLAlchemyConfig
from quart_sqlalchemy.framework import QuartSQLAlchemy

db = QuartSQLAlchemy(
    config=SQLAlchemyConfig(
        binds=dict(
            default=dict(
                engine=dict(
                    url=Config.DATABASEURL,
                    echo=True,
                    connect_args=dict(check_same_thread=False),
                ),
                session=dict(
                    expire_on_commit=False,
                ),
            )
        )
    )
)

class PersonalBaseInformationsTable(db.Model):
    __tablename__ = "PersonalBaseInformations"
    FirstName:  Mapped[int]                = mapped_column(primary_key=True)
    LastName:   Mapped[str]                = mapped_column(primary_key=True)
    Nickname:   Mapped[str]                = mapped_column(primary_key=True)
    CrewMember: Mapped["CrewMemberTable"]  = relationship()

class DutyTable(db.Model):
    __tablename__ = "Duty"
    Name:        Mapped[str] = mapped_column(primary_key=True)
    Description: Mapped[str]

class RankTable(db.Model):
    __tablename__ = "Rank"
    Name:        Mapped[str] = mapped_column(primary_key=True)
    Description: Mapped[str]

class DivisionTable(db.Model):
    __tablename__ = "Division"
    Name:        Mapped[str] = mapped_column(primary_key=True)
    Description: Mapped[str]

class CrewMemberTable(db.Model):
    __tablename__ = "CrewMember"
    Serial:                   Mapped[int]                             = mapped_column(primary_key=True,autoincrement=True)
    Nickname:                 Mapped[str]                             = mapped_column(ForeignKey("PersonalBaseInformations.Nickname"))
    PersonalBaseInformations: Mapped["PersonalBaseInformationsTable"] = relationship()
    Rank:                     Mapped["CrewMemberRankTable"]           = relationship()
    Division:                 Mapped["CrewMemberDivisionTable"]       = relationship()
    Duties:                   Mapped[list["CrewMemberDutyTable"]]     = relationship()

class CrewMemberRankTable(db.Model):
    __tablename__ = "CreMemberRank"
    id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str]               = mapped_column(ForeignKey("CrewMember.Nickname"))
    Rank:       Mapped[str]               = mapped_column(ForeignKey("Rank.Name"))
    Member:     Mapped["CrewMemberTable"] = relationship()

class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDuty"
    id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str]               = mapped_column(ForeignKey("CrewMember.Nickname"))
    Duty:       Mapped[str]               = mapped_column(ForeignKey("Duty.Name"))
    Member:     Mapped["CrewMemberTable"] = relationship()

class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivision"
    id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str]               = mapped_column(ForeignKey("CrewMember.Nickname"))
    Division:   Mapped[str]               = mapped_column(ForeignKey("Division.Name"))
    Member:     Mapped["CrewMemberTable"] = relationship()

class TaskTable(db.Model):
    __tablename__ = "Task"
    Name:             Mapped[str] = mapped_column(primary_key=True)
    Description:      Mapped[str]
    Objective:        Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]

class MissionBaseInformationTable(db.Model):
    __tablename__ = "MissionBaseInformation"
    Name:             Mapped[str] = mapped_column(primary_key=True)
    Description:      Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]

class MissionTable(db.Model):
    __tablename__ = "Mission"
    id:   Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Name: Mapped[str] = mapped_column(ForeignKey("MissionBaseInformation.Name"))
    Task: Mapped[str] = mapped_column(ForeignKey("Task.Name"))

class MemberDutyLogEntryTable(db.Model):
    __tablename__ = "MemberDutyLogEntry"
    id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Duty:       Mapped[str] = mapped_column(ForeignKey("Duty.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberOnboardLogEntryTable(db.Model):
    __tablename__ = "MemberOnboardLogEntry"
    id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Period:     Mapped[int]

class MemberRankLogEntryTable(db.Model):
    __tablename__ = "MemberRankLogEntry"
    id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Rank:       Mapped[str] = mapped_column(ForeignKey("Rank.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberDivisionLogEntryTable(db.Model):
    __tablename__ = "MemberDivisionLogEntry"
    id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Division:   Mapped[str] = mapped_column(ForeignKey("Division.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberTaskLogEntryTable(db.Model):
    __tablename__ = "MemberTaskLogEntry"
    id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Task:       Mapped[str] = mapped_column(ForeignKey("Task.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberMissionLogEntryTable(db.Model):
    __tablename__ = "MemberMissionLogEntry"
    id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Mission:    Mapped[str] = mapped_column(ForeignKey("Mission.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

db.create_all()

def selectCrew(member=""):
    if member == "":
        return select(CrewMemberTable.Nickname).distinct(CrewMemberTable.Nickname)
    else:
        members = ""
        for i in member:
            members = members + ' OR ' + i
        members = members.strip(' OR ')
        members = '\"' + members + '\"'
        print(members)
        return select(CrewMemberTable.Nickname,PersonalBaseInformationsTable.FirstName,PersonalBaseInformationsTable.LastName,CrewMemberRankTable.Rank,CrewMemberDutyTable.Duty,CrewMemberDivisionTable.Division).distinct(CrewMemberTable.Nickname).where(CrewMemberTable.Nickname==members)

def selectRank(rank=""):
    if rank == "":
        return select(RankTable)
    else:
        ranks = ""
        for i in rank:
            ranks = ranks + ' OR ' + i
        ranks = ranks.strip(' OR ')
        ranks = '\"' + ranks + '\"'
        print(ranks)
        return select(RankTable).where(RankTable.Name==ranks)

def selectDuties(duty=""):
    print(divisions)
    if duty == "":
        return select(DutyTable)
    else:
        duties = ""
        for i in duty:
            duties = duties + ' OR ' + i
        duties = duties.strip(' OR ')
        duties = '\"' + duties + '\"'
        return select(DutyTable).where(DutyTable.Name==duties)

def selectDivision(division=""):
    if division == "":
        return select(DivisionTable)
    else:

        return select(DivisionTable).where(DivisionTable.Name==division)
