from config                     import Config
from sqlalchemy.orm             import Mapped, mapped_column,DeclarativeBase,relationship
from sqlalchemy                 import ForeignKey,select,text
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
    CrewMember: Mapped["CrewMemberTable"]  = relationship()
    Id:         Mapped[int]                = mapped_column(primary_key=True,autoincrement=True)
    Nickname:   Mapped[str]                = mapped_column(unique=True)
    FirstName:  Mapped[int]
    LastName:   Mapped[str]

class DutyTable(db.Model):
    __tablename__ = "Duty"
    CrewMemberDuty: Mapped["CrewMemberDutyTable"] = relationship()
    Name:           Mapped[str]                   = mapped_column(primary_key=True)
    Description:    Mapped[str]

class RankTable(db.Model):
    __tablename__ = "Rank"
    CrewMemberRank: Mapped["CrewMemberRankTable"] = relationship()
    Name:           Mapped[str]                   = mapped_column(primary_key=True)
    Description:    Mapped[str]

class DivisionTable(db.Model):
    __tablename__ = "Division"
    CrewMemberDivision: Mapped["CrewMemberDivisionTable"] = relationship()
    Name:               Mapped[str]                       = mapped_column(primary_key=True)
    Description:        Mapped[str]

class CrewMemberRankTable(db.Model):
    __tablename__ = "CrewMemberRank"
    Member:       Mapped["CrewMemberTable"] = relationship()
    Rank:         Mapped["RankTable"]       = relationship()
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    RankName:     Mapped[str]               = mapped_column(ForeignKey("Rank.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDuty"
    Member:       Mapped["CrewMemberTable"] = relationship()
    Duty:         Mapped["DutyTable"]       = relationship()
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DutyName:     Mapped[str]               = mapped_column(ForeignKey("Duty.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivision"
    Division:     Mapped["DivisionTable"]   = relationship()
    Member:       Mapped["CrewMemberTable"] = relationship()
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DivisionName: Mapped[str]               = mapped_column(ForeignKey("Division.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberTable(db.Model):
    __tablename__ = "CrewMember"
    PersonalBaseInformations:   Mapped["PersonalBaseInformationsTable"] = relationship()
    Rank:                       Mapped["CrewMemberRankTable"]           = relationship()
    Division:                   Mapped["CrewMemberDivisionTable"]       = relationship()
    Duties:                     Mapped[list["CrewMemberDutyTable"]]     = relationship()
    PersonalBaseInformationsId: Mapped[int]                             = mapped_column(ForeignKey("PersonalBaseInformations.Id"))
    Serial:                     Mapped[int]                             = mapped_column(primary_key=True,autoincrement=True)

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
    Id:   Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    Name: Mapped[str] = mapped_column(ForeignKey("MissionBaseInformation.Name"))
    Task: Mapped[str] = mapped_column(ForeignKey("Task.Name"))

class MemberDutyLogEntryTable(db.Model):
    __tablename__ = "MemberDutyLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Duty:       Mapped[str] = mapped_column(ForeignKey("Duty.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberOnboardLogEntryTable(db.Model):
    __tablename__ = "MemberOnboardLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Period:     Mapped[int]

class MemberRankLogEntryTable(db.Model):
    __tablename__ = "MemberRankLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Rank:       Mapped[str] = mapped_column(ForeignKey("Rank.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberDivisionLogEntryTable(db.Model):
    __tablename__ = "MemberDivisionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Division:   Mapped[str] = mapped_column(ForeignKey("Division.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberTaskLogEntryTable(db.Model):
    __tablename__ = "MemberTaskLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Task:       Mapped[str] = mapped_column(ForeignKey("Task.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberMissionLogEntryTable(db.Model):
    __tablename__ = "MemberMissionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Serial"))
    Mission:    Mapped[str] = mapped_column(ForeignKey("Mission.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

db.create_all()

def selectPerson(person=""):
    if person == "":
        return None
    else:
        where_clause = f"PersonalBaseInformations.Nickname='{person}'"
        return select(PersonalBaseInformationsTable).where(text(where_clause))

def selectCrew(member=""):
    if member == "":
        return select(PersonalBaseInformationsTable.Nickname).distinct(PersonalBaseInformationsTable.Nickname)
    else:
        where_clause = f"PersonalBaseInformations.Nickname='{member}'"
        return select(PersonalBaseInformationsTable.FirstName.label('FirstName'),
                        PersonalBaseInformationsTable.LastName.label('LastName'),
                        PersonalBaseInformationsTable.Nickname.label('Nickname'),
                        CrewMemberRankTable.RankName.label('Rank'),
                        CrewMemberDutyTable.DutyName.label('Duty'),
                        CrewMemberDivisionTable.DivisionName.label('Division')
                    ).join(CrewMemberTable,PersonalBaseInformationsTable.Id==CrewMemberTable.PersonalBaseInformationsId)\
                    .join(CrewMemberRankTable,CrewMemberTable.Serial==CrewMemberRankTable.MemberSerial)\
                    .join(RankTable,CrewMemberRankTable.RankName==RankTable.Name)\
                    .join(CrewMemberDutyTable,CrewMemberTable.Serial==CrewMemberDutyTable.MemberSerial)\
                    .join(DutyTable,CrewMemberDutyTable.DutyName==DutyTable.Name)\
                    .join(CrewMemberDivisionTable,CrewMemberTable.Serial==CrewMemberDivisionTable.MemberSerial)\
                    .join(DivisionTable,CrewMemberDivisionTable.DivisionName==DivisionTable.Name)\
                    .where(text(where_clause))

def selectRank(rank=""):
    if rank == "":
        return select(RankTable)
    else:
        where_clause = f"Rank.Name='{rank}'"
        return select(RankTable).where(text(where_clause))

def selectDuty(duty=""):
    if duty == "":
        return select(DutyTable)
    else:
        where_clause = f"Duty.Name='{duty}'"
        return select(DutyTable).where(text(where_clause))

def selectDivision(division=""):
    if division == "":
        return select(DivisionTable)
    else:
        where_clause = f"Division.Name='{division}''"
        return select(DivisionTable).where(text(where_clause))
