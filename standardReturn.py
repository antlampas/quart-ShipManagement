from quart import render_template
from quart import session

async def standardReturn(template="index.html",sectionName="Home Page",**args):
    if 'auth_token' in session:
        return await render_template(template,SECTIONNAME=sectionName,SESSION=session,**args)
    else:
        return await render_template(template,SECTIONNAME=sectionName,**args)
