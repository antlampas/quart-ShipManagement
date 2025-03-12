from quart_wtf          import QuartForm,CSRFProtect
from wtforms            import StringField,PasswordField,SelectField,SelectMultipleField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.widgets    import PasswordInput

class AddCrewMemberForm(QuartForm):
    FirstName        = StringField('First name')
    LastName         = StringField('Last Name')
    Nickname         = StringField('Nickname')
    Rank             = SelectField('Rank')
    Division         = SelectField('Division')
    Duties           = SelectMultipleField('Duties')

class RemoveCrewMemberForm(QuartForm):
    Nickname         = SelectMultipleField('Member')

class EditCrewMemberForm(QuartForm):
    FirstName        = StringField('First name')
    LastName         = StringField('Last Name')
    Nickname         = StringField('Nickname')
    Rank             = SelectField('Rank')
    Division         = SelectField('Division')
    Duties           = SelectMultipleField('Duties')

class AddTaskForm(QuartForm):
    Name             = StringField('Task')
    Description      = StringField('Description')
    Objective        = StringField('Objective')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Status           = StringField('Status')

class RemoveTaskForm(QuartForm):
    Name             = SelectMultipleField('Task')

class EditTaskForm(QuartForm):
    Name             = StringField('Task')
    Description      = StringField('Description')
    Objective        = StringField('Objective')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Status           = StringField('Status')

class AddMissionForm(QuartForm):
    Name             = StringField('Mission')
    Description      = StringField('Description')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Tasks            = SelectMultipleField('Tasks')
    Status           = StringField('Status')

class RemoveMissionForm(QuartForm):
    Name             = SelectMultipleField('Mission')

class EditMissionForm(QuartForm):
    Name             = StringField('Mission')
    Description      = StringField('Description')
    RequiredDuration = StringField('Required Duration')
    StartedAt        = StringField('Started At')
    EndedAt          = StringField('Ended At')
    Tasks            = SelectMultipleField('Tasks')
    Status           = StringField('Status')

class AddRankForm(QuartForm):
    Name        = StringField('Rank')
    Description = StringField('Description')

class EditRankForm(QuartForm):
    Name        = StringField('Rank')
    Description = StringField('Description')

class RemoveRankForm(QuartForm):
    Name = SelectMultipleField('Rank')

class AddDutyForm(QuartForm):
    Name        = StringField('Task')
    Description = StringField('Description')

class EditDutyForm(QuartForm):
    Name        = StringField('Task')
    Description = StringField('Description')

class RemoveDutyForm(QuartForm):
    Name = SelectMultipleField('Rank')

class AddDivisionForm(QuartForm):
    Name        = StringField('Division')
    Description = StringField('Description')

class EditDivisionForm(QuartForm):
    Name        = StringField('Division')
    Description = StringField('Description')

class RemoveDivisionForm(QuartForm):
    Name = SelectMultipleField('Division')
