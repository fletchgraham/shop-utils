from invoke import task

from mockup_automator import main

@task
def mockup(c, name="Fletch"):
    main()
