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
    CrewMember: Mapped["CrewMemberTable"]  = relationship(back_populates="PersonalBaseInformations")

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
    PersonalBaseInformations: Mapped["PersonalBaseInformationsTable"] = relationship(back_populates="Nickname")
    Rank:                     Mapped["CrewMemberRankTable"]           = relationship(back_populates="Name")
    Division:                 Mapped["CrewMemberDivisionTable"]       = relationship(back_populates="Name")
    Duties:                   Mapped[list["CrewMemberDutyTable"]]     = relationship(back_populates="Name")

class CrewMemberRankTable(db.Model):
    __tablename__ = "CreMemberRank"
    id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str]               = mapped_column(ForeignKey("CrewMember.Nickname"))
    Rank:       Mapped[str]               = mapped_column(ForeignKey("Rank.Name"))
    Member:     Mapped["CrewMemberTable"] = relationship(back_populates="Nickname")

class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDuty"
    id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str]               = mapped_column(ForeignKey("CrewMember.Nickname"))
    Duty:       Mapped[str]               = mapped_column(ForeignKey("Duty.Name"))
    Member:     Mapped["CrewMemberTable"] = relationship(back_populates="Nickname")

class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivision"
    id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    CrewMember: Mapped[str]               = mapped_column(ForeignKey("CrewMember.Nickname"))
    Division:   Mapped[str]               = mapped_column(ForeignKey("Division.Name"))
    Member:     Mapped["CrewMemberTable"] = relationship(back_populates="Nickname")

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
        where_clause = f"CrewMember.Name='{member}'"
        return select(CrewMemberTable).where(where_clause)

def selectRank(rank=""):
    if rank == "":
        return select(RankTable)
    else:
        where_clause = f"Rank.Name='{rank}'"
        return select(RankTable).where(where_clause)

def selectDuty(duty=""):
    if duty == "":
        return select(DutyTable)
    else:
        where_clause = f"Duty.Name='{duty}'"
        return select(DutyTable).where(where_clause)

def selectDivision(division=""):
    if division == "":
        return select(DivisionTable)
    else:
        where_clause = f"Division.Name='{division}''"
        return select(DivisionTable).where(where_clause)
