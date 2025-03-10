from quart-wtf          import QuartForm,CSRFProtect
from wtforms            import TextField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.widgets    import PasswordInput

class AddCrewMemberForm(QuartForm):
    FirstName        = TextField('First name')
    LastName         = TextField('Last Name')
    Nickname         = TextField('Nickname')

class RemoveCrewMemberForm(QuartForm):
    Nickname         = SelectMultipleField('Member')

class EditCrewMemberForm(QuartForm):
    FirstName        = TextField('First name')
    LastName         = TextField('Last Name')
    Nickname         = TextField('Nickname')

class AddTaskForm(QuartForm):
    Name             = TextField('Task')
    Description      = TextField('Description')
    Objective        = TextField('Objective')
    RequiredDuration = TextField('Required Duration')
    StartedAt        = TextField('Started At')
    EndedAt          = TextField('Ended At')
    Status           = TextField('Status')

class RemoveTaskForm(QuartForm):
    Name             = SelectMultipleField('Task')

class EditTaskForm(QuartForm):
    Name             = TextField('Task')
    Description      = TextField('Description')
    Objective        = TextField('Objective')
    RequiredDuration = TextField('Required Duration')
    StartedAt        = TextField('Started At')
    EndedAt          = TextField('Ended At')
    Status           = TextField('Status')

class AddMissionForm(QuartForm):
    Name             = TextField('Mission')
    Description      = TextField('Description')
    RequiredDuration = TextField('Required Duration')
    StartedAt        = TextField('Started At')
    EndedAt          = TextField('Ended At')
    Tasks            = SelectMultipleField('Tasks')
    Status           = TextField('Status')

class RemoveMissionForm(QuartForm):
    Name             = SelectMultipleField('Mission')

class EditMissionForm(QuartForm):
    Name             = TextField('Mission')
    Description      = TextField('Description')
    RequiredDuration = TextField('Required Duration')
    StartedAt        = TextField('Started At')
    EndedAt          = TextField('Ended At')
    Tasks            = SelectMultipleField('Tasks')
    Status           = TextField('Status')
