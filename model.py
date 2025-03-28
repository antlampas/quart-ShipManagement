from config                     import Config
from sqlalchemy                 import ForeignKey
from sqlalchemy                 import select
from sqlalchemy                 import text
from sqlalchemy.orm             import Mapped
from sqlalchemy.orm             import mapped_column
from sqlalchemy.orm             import DeclarativeBase
from sqlalchemy.orm             import relationship
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
    CrewMember: Mapped["CrewMemberTable"] = relationship(cascade='all,delete')
    Id:         Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    Nickname:   Mapped[str]               = mapped_column(unique=True)
    FirstName:  Mapped[int]
    LastName:   Mapped[str]

class DutyTable(db.Model):
    __tablename__ = "Duty"
    CrewMemberDuty: Mapped["CrewMemberDutyTable"] = relationship(cascade='all,delete')
    Name:           Mapped[str]                   = mapped_column(primary_key=True)
    Description:    Mapped[str]

class RankTable(db.Model):
    __tablename__ = "Rank"
    CrewMemberRank: Mapped["CrewMemberRankTable"] = relationship(cascade='all,delete')
    Name:           Mapped[str]                   = mapped_column(primary_key=True)
    Description:    Mapped[str]

class DivisionTable(db.Model):
    __tablename__ = "Division"
    CrewMemberDivision:          Mapped["CrewMemberDivisionTable"]          = relationship(cascade='all,delete')
    CrewMemberSecondaryDivision: Mapped["CrewMemberSecondaryDivisionTable"] = relationship(cascade='all,delete')
    Name:                        Mapped[str]                                = mapped_column(primary_key=True)
    Description:                 Mapped[str]

class CrewMemberRankTable(db.Model):
    __tablename__ = "CrewMemberRank"
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete')
    Rank:         Mapped["RankTable"]       = relationship(cascade='all,delete')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    RankName:     Mapped[str]               = mapped_column(ForeignKey("Rank.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDuty"
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete')
    Duty:         Mapped["DutyTable"]       = relationship(cascade='all,delete')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DutyName:     Mapped[str]               = mapped_column(ForeignKey("Duty.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivision"
    Division:     Mapped["DivisionTable"]   = relationship(cascade='all,delete')
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DivisionName: Mapped[str]               = mapped_column(ForeignKey("Division.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberSecondaryDivisionTable(db.Model):
    __tablename__ = "CrewMemberSecondaryDivision"
    Division:     Mapped["DivisionTable"]   = relationship(cascade='all,delete')
    Member:       Mapped["CrewMemberTable"] = relationship(cascade='all,delete')
    Id:           Mapped[int]               = mapped_column(primary_key=True,autoincrement=True)
    DivisionName: Mapped[str]               = mapped_column(ForeignKey("Division.Name"))
    MemberSerial: Mapped[int]               = mapped_column(ForeignKey("CrewMember.Serial"))

class CrewMemberTable(db.Model):
    __tablename__ = "CrewMember"
    PersonalBaseInformations:   Mapped["PersonalBaseInformationsTable"] = relationship(cascade='all,delete')
    Rank:                       Mapped["CrewMemberRankTable"]           = relationship(cascade='all,delete')
    Division:                   Mapped["CrewMemberDivisionTable"]       = relationship(cascade='all,delete')
    Duties:                     Mapped[list["CrewMemberDutyTable"]]     = relationship(cascade='all,delete')
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

def selectCrew(member=""):
    if member == "":
        return select(PersonalBaseInformationsTable)
    else:
        where_clause = f"PersonalBaseInformations.Nickname='{member}'"
        return select(
            PersonalBaseInformationsTable.FirstName.label('FirstName'),
            PersonalBaseInformationsTable.LastName.label('LastName'),
            PersonalBaseInformationsTable.Nickname.label('Nickname'),
            CrewMemberTable.Serial.label('Serial'),
            CrewMemberRankTable.RankName.label('Rank'),
            CrewMemberDutyTable.DutyName.label('Duty'),
            CrewMemberDivisionTable.DivisionName.label('Division')
        ).join(
            CrewMemberTable,
            PersonalBaseInformationsTable.Id == CrewMemberTable.PersonalBaseInformationsId
        ).join(
            CrewMemberRankTable,
            CrewMemberTable.Serial == CrewMemberRankTable.MemberSerial
        ).join(
            CrewMemberDutyTable,
            CrewMemberTable.Serial == CrewMemberDutyTable.MemberSerial
        ).join(
            CrewMemberDivisionTable,
            CrewMemberTable.Serial == CrewMemberDivisionTable.MemberSerial
        ).where(text(where_clause))

def selectPerson(person=""):
    if person == "":
        return None
    else:
        where_clause = f"PersonalBaseInformations.Nickname='{person}'"
        return select(PersonalBaseInformationsTable).where(text(where_clause))


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
