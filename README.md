# powerapps-docstring

PowerApps-docstring ist an console based, pipeline ready application that automatically generates user and technical documentation for PowerApps.

**Currently in "call for demands/ideas" stage**

## Purpose of this application
Documentation of Microsoft Power Apps is an important building block in the software lifecycle. As in the traditional software development process, the developed Power App should also be documented propperly to ensure further development/support and maintenance as well as onboarding of new developers.

Unfortunately, it is currently not possible to automatically create documentation for a Power App "out of the box" based on the App (code) itself. 
Resolving in either hours of manual documentation work or a lack of propper documentation.

This application shall solve this problem by providing a way to:
- create Power Apps documentation based on the code and comments provided inside the app development process itself
- integrate the documentation creation process into the ci/cd pipeline aswell as
- create documentation based on an exported app

## Feature ideas
If you would like to submit your idea, please comment this issue: https://github.com/sebastian-muthwill/powerapps-docstring/issues/1

- screenflow from navigations
- screen descriptions from comments
- used functions  (configurable)
- comments
- used connections
- output
  - user and technical documentation
  - markdown
  - html
  - pdf
- handels the following formats:
  - zip
  - mssap
  - src
- usable via Azure DevOps CI-CD pipeline

## Todos
- collect ideas
- create first alpha version

## Follow this topic
[Twitter](https://twitter.com/waszumkuckuck)

#powerapps_docstring #PowerAtelier #CloudCouchRocks 
