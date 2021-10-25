# powerapps-docstring

PowerApps-docstring is a console based, pipeline ready application that automatically generates user and technical documentation for PowerApps.

> A first version of a Power Apps Documentation Guideline is available here: [Power Apps Documentation Guideline](docu/PoweApps_Documentation_Guideline.md)

## Purpose of this application
Documentation of Microsoft Power Apps is an important building block in the software lifecycle. As in the traditional software development process, the developed Power App should also be documented propperly to ensure further development/support and maintenance as well as onboarding of new developers.

Unfortunately, it is currently not possible to automatically create documentation for a Power App "out of the box" based on the App (code) itself. 
Resolving in either hours of manual documentation work or a lack of propper documentation at all.

This application shall solve this problem by providing a way to:
- create Power Apps documentation based on the code and docstrings provided inside the app development process itself
- integrate the documentation creation process into the ci/cd pipeline aswell as
- create documentation based on an exported app

## Getting started
1. clone repository `git clone https://github.com/sebastian-muthwill/powerapps-docstring.git` and change into directory `cd powerapps-docstring`
2. install requirements with `pip install -r requirements.txt`
3. run with `python3 main.py -s example/src/meetingcapturedemo -o example`

Once the application finished successfully the documentation file is created in the specified folder in markdown format.

### Example
The example [Meeting Capture Demo-doc.md](example/Meeting Capture Demo-doc.md) is based on the template "Meeting Capture App" provided by Microsoft. The app has not been modified except docstrings have been added within the `OnVisible` propperties of each screen as well as `OnStart`. The source files are also available in the example folder.

![PowerApps_Docstring_demo](https://user-images.githubusercontent.com/10375725/137876032-42aea559-bd16-4c23-a15d-4512dd12f524.gif)


### Known issues / optimizations
- screens are not in the order as in Power Apps Studio see: #10
- mermaid graph looks wierd whe to many screens and is not displayed in github since github currently does not support mermaid
- currently not tested with modell driven apps

## Feature ideas
If you would like to submit your idea, feel free to create an issue.

- ~~screen descriptions from comments~~
- ~~screenflow from navigations~~
- ~~used functions  (configurable)~~
- ~~used connections~~
- output
  - user ~~and technical~~ documentation
  - ~~markdown~~
  - html
  - pdf
- handle following formats:
  - zip
  - mssap
  - ~~src~~
- usable via Azure DevOps CI-CD pipeline (not tested yet)

## Follow this topic
Get in touch with me on: [Twitter](https://twitter.com/waszumkuckuck)

#powerapps_docstring #PowerAtelier #CloudCouchRocks 
