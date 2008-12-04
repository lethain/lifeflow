
### Welcome to LifeFlow

LifeFlow is an opinionated blogging application written
on top of the [Django](http://djangoproject.com) web
framework.

### 1.0 to 2.0

Before this pre-2.0 branch, there was the pre-1.0 branch.
The 1.0 branch suffered from massive complexity, and the
primary focus of the 2.0 branch is to restructure LifeFlow's
code to make it easier to work with and less complex.

### Contents of Project

*  ``example_project`` contains a sample LifeFlow project.
*  ``lifeflow_core`` is contains core LifeFlow functionality.
   You must have core installed to use other apps.
*  ``lifeflow_blog`` is the blogging software itself.
*  ``lifeflow_api`` is an optional app which allows
    other applications to manipulate LifeFlow.
*  ``lifeflow_editor`` is a full-featured editor which
    is based on the ``lifeflow_api``.

### Setup & Usage

1.  Add all applications to Python path.
    
        ln -s /Users/will/git/lifeflow/lifeflow_core /Library/Python/2.5/site-packages/lifeflow_core
        ln -s /Users/will/git/lifeflow/lifeflow_blog /Library/Python/2.5/site-packages/lifeflow_blog
        ln -s /Users/will/git/lifeflow/lifeflow_api /Library/Python/2.5/site-packages/lifeflow_api
        ln -s /Users/will/git/lifeflow/lifeflow_editor /Library/Python/2.5/site-packages/lifeflow_editor


2.  Sym-link contents of application media folders
    into your project's media folder.
3.  Run sync-db.
4.  Customize...
5.  Profits...
