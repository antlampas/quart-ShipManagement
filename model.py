from config                     import Config
from sqlalchemy.orm             import Mapped, mapped_column,DeclarativeBase,relationship
from sqlalchemy                 import ForeignKey
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

class Base(DeclarativeBase):
    pass

class PersonalBaseInformationsTable(db.Model):
    __tablename__ = "Personaldb.ModelInformations"
    FirstName: Mapped[int] = mapped_column(primary_key=True)
    LastName:  Mapped[str] = mapped_column(primary_key=True)
    Nickname:  Mapped[str] = mapped_column(primary_key=True)

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
    Serial:   Mapped[str] = mapped_column(primary_key=True)
    Nickname: Mapped[str] = mapped_column(ForeignKey("Personaldb.ModelInformations.Nickname"))

class CrewMemberRankTable(db.Model):
    __tablename__ = "CreMemberRankTable"
    id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Rank:       Mapped[str] = mapped_column(ForeignKey("Rank.Name"))

class CrewMemberDutyTable(db.Model):
    __tablename__ = "CrewMemberDutyTable"
    id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Duty:       Mapped[str] = mapped_column(ForeignKey("Duty.Name"))

class CrewMemberDivisionTable(db.Model):
    __tablename__ = "CrewMemberDivisionTable"
    id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Division:   Mapped[str] = mapped_column(ForeignKey("Division.Name"))

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
    __tablename__ = "Missiondb.ModelInformation"
    Name:             Mapped[str] = mapped_column(primary_key=True)
    Description:      Mapped[str]
    RequiredDuration: Mapped[str]
    StartedAt:        Mapped[int]
    EndedAt:          Mapped[int]
    Status:           Mapped[str]

class MissionTable(db.Model):
    __tablename__ = "Mission"
    Id:   Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(ForeignKey("Missiondb.ModelInformation.Name"))
    Task: Mapped[str] = mapped_column(ForeignKey("Task.Name"))

class MemberDutyLogEntryTable(db.Model):
    __tablename__ = "MemberDutyLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Duty:       Mapped[str] = mapped_column(ForeignKey("Duty.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberOnboardLogEntryTable(db.Model):
    __tablename__ = "MemberOnboardLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Period:     Mapped[int]

class MemberRankLogEntryTable(db.Model):
    __tablename__ = "MemberRankLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Rank:       Mapped[str] = mapped_column(ForeignKey("Rank.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberDivisionLogEntryTable(db.Model):
    __tablename__ = "MemberDivisionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Division:   Mapped[str] = mapped_column(ForeignKey("Division.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberTaskLogEntryTable(db.Model):
    __tablename__ = "MemberTaskLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Task:       Mapped[str] = mapped_column(ForeignKey("Task.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

class MemberMissionLogEntryTable(db.Model):
    __tablename__ = "MemberMissionLogEntry"
    Id:         Mapped[int] = mapped_column(primary_key=True)
    CrewMember: Mapped[str] = mapped_column(ForeignKey("CrewMember.Nickname"))
    Mission:    Mapped[str] = mapped_column(ForeignKey("Mission.Name"))
    Period:     Mapped[int]
    Status:     Mapped[str]
    Grade:      Mapped[str]

db.create_all()

PersonalBaseInformationsTable.crewmember = relationship(CrewMemberTable,order_by=PersonalBaseInformationsTable.Nickname)
DutyTable.crewmember                     = relationship(CrewMemberTable,order_by=DutyTable.Name)
RankTable.crewmember                     = relationship(CrewMemberTable,order_by=RankTable.Name)
DutyTable.memberdutylogentry             = relationship(MemberDutyLogEntryTable,order_by=DutyTable.Name)
CrewMemberTable.memberdutylogentry       = relationship(MemberDutyLogEntryTable,order_by=CrewMemberTable.Nickname)
RankTable.memberranklogEntry             = relationship(MemberRankLogEntryTable,order_by=RankTable.Name)
CrewMemberTable.memberranklogEntry       = relationship(MemberRankLogEntryTable,order_by=CrewMemberTable.Nickname)
