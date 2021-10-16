
Power App Documentation
=======================

Contents
========

* [Meeting Capture Demo](#meeting-capture-demo)
	* [OnStart](#onstart)
* [Connections](#connections)
* [Screens](#screens)
	* [AttachmentsScreen](#attachmentsscreen)
	* [CameraScreen](#camerascreen)
	* [CollectionsAndVariables](#collectionsandvariables)
	* [ConfirmScreen](#confirmscreen)
	* [EmailScreen](#emailscreen)
	* [ExportPopUpsScreen](#exportpopupsscreen)
	* [ExportScreen](#exportscreen)
	* [FollowUpScreen](#followupscreen)
	* [FollowUpTimesScreen](#followuptimesscreen)
	* [HomePopUpsScreen](#homepopupsscreen)
	* [HomeScreen](#homescreen)
	* [SketchScreen](#sketchscreen)
	* [WelcomeScreen](#welcomescreen)
  
  

# Meeting Capture Demo


 An all-in-one meeting capture tool.
![](src\meetingcapturedemo\Assets\Images\meeting-capture-logo-full%403x.png)

This 
tool helps you to keep everythin in one place during your meetings.

Key features are:
- View meeting details
- capture 
notes and pictures of whiteboards
- assign tasks
- send meeeting notes to all attendees in one click

  

## OnStart


```
Collect(CalendarLocalizedLabel,      {Value:"Calendar"},{Value:"Kalender"},
{Value:"Təqvim"},{Value:"Kalendar"},{Value:"Calendari"},{Value:"Kalendář"},{Value:"Calendr"},{Value:"Calendario"},
{Value:"Egutegia"},{Value:"Kalendaryo"},{Value:"Calendrier"},{Value:"Féilire"},{Value:"Am mìosachan"},{Value:"Kalanda"},
{Value:"Dagbók"},{Value:"Kalenda"},{Value:"Kalendārs"},{Value:"Kalenner"},{Value:"Kalendorius"},{Value:"Naptár"},
{Value:"Kalendarju"},{Value:"Agenda"},{Value:"Taqvim"},{Value:"Kalendarz"},{Value:"Calendário"},{Value:"Intiwatana"},
{Value:"Kalendari"},{Value:"Kalendár"},{Value:"Koledar"},{Value:"Kalenteri"},{Value:"Maramataka"},{Value:"Lịch"},
{Value:"Takvim"},{Value:"Senenama"},{Value:"Ημερολόγιο"},{Value:"კალენდარი"},{Value:"לוח שנה"},{Value:"کیلنڈر"},
{Value:"التقويم"},{Value:"कैलेंडर"},{Value:"दिनदर्शिका"},{Value:"ক্যালেন্ডার"},{Value:"કૅલેન્ડર"},{Value:"予定表"},
{Value:"行事曆"},{Value:"日历"},{Value:"క్యాలెండర్"});

Concurrent(Set(MyCalendarID,LookUp(Office365Outlook.CalendarGetTables().value,DisplayName=LookUp(CalendarLocalizedLabel,Value=DisplayName).Value).Name);ClearCollect(AllFutureEvents,Office365Outlook.GetEventsCalendarView(MyCalendarID,Text(Today(),UTC),Text(DateAdd(Today(),2,Days),UTC)).Values),Set(MyUserProfile,Office365Users.MyProfile().Id),
    /*used to determine if meeting attendees are in app user's org*/
Set(MyDomain,Last(Split(User().Email,"@")).Result),
    /*used to determine countdown to end of selected meeting*/
Set(HomeTimerStart,Now()));
/*Meetings are defined to be calendar events less than 6 hours in length*/
ClearCollect(MeetingsOnly,Filter(AddColumns(AllFutureEvents,"isCurrent",DateDiff(Start,Now(),Seconds)>0&&DateDiff(Now(),End,Seconds)>0),DateDiff(Start,End,Hours)<6));Set(NumberOfCurrentMeetings,CountRows(Filter(MeetingsOnly,isCurrent)));
/*If a single meeting is happening now, autoselect it*/
If(NumberOfCurrentMeetings=1,Set(AutoSelectMeeting, true );Set(SelectedMeeting,LookUp(MeetingsOnly,isCurrent)))
```
# Connections
  
**OneNote (Business) (Standard)**  
  
sku: Enterprise  
  
With following datasources:  

- OneNote(Business)
  
  
**Planner (Standard)**  
  
sku: Enterprise  
  
With following datasources:  

- Planner
  
  
**Office 365 Users (Standard)**  
  
sku: Enterprise  
  
With following datasources:  

- Office365Users
  
  
**Office 365 Outlook**  
  
sku: Enterprise  
  
With following datasources:  

- Office365Outlook
  

# Screens
  
:::mermaid  
graph LR  
CameraScreen ==> HomeScreen  
CameraScreen ==> SketchScreen  
ConfirmScreen ==> HomeScreen  
ConfirmScreen ==> FollowUpScreen  
ConfirmScreen ==> WelcomeScreen  
EmailScreen ==> ConfirmScreen  
ExportPopUpsScreen ==> ExportScreen  
ExportPopUpsScreen ==> ConfirmScreen  
ExportScreen ==> HomeScreen  
ExportScreen ==> ExportPopUpsScreen  
FollowUpScreen ==> FollowUpTimesScreen  
FollowUpTimesScreen ==> ConfirmScreen  
HomePopUpsScreen ==> HomeScreen  
HomeScreen ==> SketchScreen  
HomeScreen ==> CameraScreen  
HomeScreen ==> EmailScreen  
HomeScreen ==> AttachmentsScreen  
HomeScreen ==> ExportScreen  
HomeScreen ==> HomePopUpsScreen  
SketchScreen ==> HomeScreen  
SketchScreen ==> CameraScreen  
WelcomeScreen ==> HomePopUpsScreen  
:::
## AttachmentsScreen
  
---
### AttachmentsScreen As screen


See attachments created during meeting
### AppLogo5 As image

#### Image


```
='nav-logo'
```
### AttachmentsHeader As label

#### Size


```
=27
```
#### Text


```
="Meeting Attachments"
```
### PhotosIcon As image

#### Image


```
='attachments-camera'
```
### PhotosHeader As label

#### Size


```
=15
```
#### Text


```
="Photos"
```
### PhotosGallery As gallery.galleryHorizontal

#### Items


```
=Photos
```
#### OnSelect


```
=Set(ShowOverlay, true);
Set(SelectedImage, ThisItem)
```
### PhotosCount As label

#### Size


```
=10.5
```
#### Text


```
=CountRows(Photos) & If(CountRows(Photos) = 1, " photo has", " photos have") & " been attached to this meeting"
```
### SketchesIcon As image

#### Image


```
='attachments-sketch'
```
### SketchesHeader As label

#### Size


```
=15
```
#### Text


```
="Sketches"
```
### SketchCount As label

#### Size


```
=10.5
```
#### Text


```
=CountRows(Sketches) & If(CountRows(Sketches) = 1, " sketch has", " sketches have") & " been attached to this meeting"
```
### SketchesGallery As gallery.galleryHorizontal

#### Items


```
=Sketches
```
#### OnSelect


```
=Set(ShowOverlay, true);
Set(SelectedImage, ThisItem)
```
### AttachmentToDelete As image

#### Image


```
=SelectedImage.Image
```
### DeleteCertaintyText As label

#### Size


```
=10.5
```
#### Text


```
="Are you sure you want to delete?"
```
### CancelDeleteAttach As button

#### OnSelect


```
=Set(AttachmentDeleteConfirm, false);
Set(ShowOverlay, false)
```
#### Text


```
=If(TaskSelected, "Delete", "Cancel")
```
### ConfirmDeleteAttach As button

#### OnSelect


```
=Set(ShowOverlay, false);
Set(AttachmentDeleteConfirm, false);
RemoveIf(Sketches, SelectedImage.Name = Name);
RemoveIf(Photos, SelectedImage.Name = Name)

```
#### Text


```
="Yes, delete"
```
## CameraScreen
  
---
### CameraScreen As screen


Take picture during a meeting
#### OnVisible


```
Set(ShowImageSaved, false);
Set(ShowTakenImage, false)
```
### AppLogo3 As image

#### Image


```
='nav-logo'
```
### NavHome3 As image

#### Image


```
='nav-notes'
```
#### OnSelect


```
=Navigate(HomeScreen, None)
```
### NavSketch3 As image

#### Image


```
='nav-sketch'
```
#### OnSelect


```
=Navigate(SketchScreen, None)
```
### NavPhotos3 As image

#### Image


```
='nav-camera'
```
### BannerText As label

#### Text


```
=If(ShowTakenImage, "Keep or discard this image?", ShowImageSaved, "Saved!", "Tap the image to take a photo")
```
## CollectionsAndVariables
  
---
### CollectionsAndVariables As screen


This screen lists all collections and variables used inside the app

## ConfirmScreen
  
---
### ConfirmScreen As screen


Export confirmation screen
Once the export is completed another meeting can be scheduled with the attendees.

#### OnVisible


```
If(ExportConfirmed,
    Set(Loading, true);

    /*Collects the dynamic data which will be substituted into the Email/OneNote templates and associates it to the {placeholder} values in the templates
       At {Field: "{1}" at <tr><td colspan='3'> changed <td colspan='3' style='height:10px;'> to <td colspan='3'> because OneNote stopped displaying the export content with the inline style content present 
    */
        If(CheckEmail.Value || CheckOneNote.Value, 
             ClearCollect(TemplateData, {Field:"{MeetingName}", Data:SelectedMeeting.Subject}, {Field: "{MeetingStartDate}", Data: Text(SelectedMeeting.Start, "[$-en-US]mmm. dd, yyyy")}, 
            {Field: "{MeetingStartTime}", Data: Lower(Text(SelectedMeeting.Start, "[$-en-US]hh:mm am/pm"))}, {Field: "{MeetingEndTime}", Data: Lower(Text(SelectedMeeting.End, "[$-en-US]hh:mm am/pm"))},
            {Field: "{MeetingMinutes}", Data: Text(SelectedMeetingDuration/60)}, {Field: "{MeetingAttendeeNum}", Data: Text(CountRows(MeetingAttendees))},
            {Field: "{1}", 
            Data: Concat(
                GroupBy(
                    ForAll(MeetingAttendees,
                        Collect(Indexes, {Index:Last(Indexes).Index + 1});
                        {Page:RoundDown(Last(Indexes).Index / 3,0),
                        Id:Id, 
                        DisplayName:DisplayName, 
                        JobTitle:JobTitle}
                    ),
            "Page","Attendees"),"<tr>" & Concat(Attendees,"<td class='user-name' width='221'>" & DisplayName & "</td>") & If(CountRows(Attendees)=2,"<td class='user-name' width='221'></td>",CountRows(Attendees)=1,
            "<td class='user-name' width='221'></td><td class='user-name' width='221'></td>") & "</tr><tr>" & Concat(Attendees,"<td class='job-title'>" & JobTitle & "</td>") & If(CountRows(Attendees)=2,
            "<td class='job-title'></td>",CountRows(Attendees)=1,"<td class='job-title'></td><td class='job-title'></td>") & "</tr><tr><td colspan='3'></td></tr>")},
            {Field: "{MeetingDetails}", Data:MeetingBody.HtmlText}, {Field: "{MeetingNotes}", Data: Substitute(NotesInput.Text, Char(10), "<br/>")},
            {Field: "{2}", Data: Concat(Tasks,"<tr><td class='task'><table border='0' cellpadding='0' cellspacing='0' class='no-border' style='table-layout:auto'><tr><td class='name'><a class='link-name' href='https://tasks.office.com' target='_blank'>" & Name & "</a></td><td class='due-time'>" & If(IsBlank(DueDate),"","Due " & If(IsToday(DueDate),"Today",Text(DueDate,"[$-en-US]mmm d"))) & "</td></tr><tr><td colspan='2' class='assign-to'>" & AssignToUser.DisplayName & "</td></tr></table></td></tr>")})
        );

        /*Creates planner tasks based on the Tasks collection*/
        If(CheckPlanner.Value,ForAll(Tasks,Planner.CreateTask(SelectedPlan.'data-ADB4D7A662F548B49FAC2B986E348A1Bid',Name,{bucketId:SelectedBucket.'data-ADB4D7A662F548B49FAC2B986E348A1Bid',dueDateTime:AssnTaskDueDate_1,assignments:AssignToUser.Id})));
        /*combines photos and sketches into a single email attachments collection*/
        If(CheckEmail.Value,
            ForAll(Photos, Collect(EmailAttachments, {ContentBytes: Image, Image: Image, Name: Name}));
            ForAll(Sketches, Collect(EmailAttachments, {ContentBytes: Image, Image: Image, Name: Name}));
        /*replaces {placeholder} values for Email template with dynamic data collected from user's input as they progress through app*/   
            ForAll(TemplateData, Patch(Templates, LookUp(Templates, Template="Email"), {Value: Substitute(LookUp(Templates, Template="Email").Value, Field, Data)}));
            Office365Outlook.SendEmail(Concat(EmailRecipients, UserPrincipalName & ";"), SelectedMeeting.Subject, LookUp(Templates, Template="Email").Value, {Attachments: EmailAttachments, Importance: "Normal", IsHtml: true}
            )    
        );
        If(CheckOneNote.Value,
        /*replaces {placeholder} values for OneNote template with dynamic data collected from user's input as they progress through app*/    
            ForAll(TemplateData, Patch(Templates, LookUp(Templates, Template="OneNote"), {Value: Substitute(LookUp(Templates, Template="OneNote").Value, Field, Data)}));
            'OneNote(Business)'.CreatePageInSection(SelectedNoteBook.'data-ADB4D7A662F548B49FAC2B986E348A1BKey', SelectedSection.'data-ADB4D7A662F548B49FAC2B986E348A1BpagesUrl', LookUp(Templates, Template="OneNote").Value)
        );

    Set(Loading, false)
)
```
## EmailScreen
  
---
### EmailScreen As screen


Email meeting notes to attendees
### BannerHeader As label

#### Size


```
=12
```
#### Text


```
=SelectedMeeting.Subject
```
### AppLogo4 As image

#### Image


```
='nav-logo'
```
### EmailBannerText As label

#### Size


```
=27
```
#### Text


```
="Email attendee" & If(MultiRecipients, "s") & ":"
```
### SendEmail As button

#### OnSelect


```
=Office365Outlook.SendEmail(Concat(EmailRecipients, UserPrincipalName & ";"), EmailSubject.Text, EmailMessage.Text, {Importance: "Normal"});
/*Sets text to display email confirmation info*/
Set(EmailConfirmed, true);
Navigate(ConfirmScreen, None)
```
#### Text


```
="Send"
```
### GalleryBkg As button

#### Text


```
=""
```
### Label16 As label

#### Size


```
=15
```
#### Text


```
="Recipient" & If(MultiRecipients, "s (" & CountRows(EmailRecipients) & ")")
```
### EmailRecipientGallery As gallery.galleryHorizontal

#### Items


```
=EmailRecipients
```
### Label16_1 As label

#### Size


```
=15
```
#### Text


```
="Subject"
```
### EmailSubject As text

### Label16_2 As label

#### Size


```
=15
```
#### Text


```
="Message"
```
### EmailMessage As text

## ExportPopUpsScreen
  
---
### ExportPopUpsScreen As screen

### OverlayHeader_1 As label

#### Size


```
=28
```
#### Text


```
=If(ShowOverlay, "Are you finished taking notes?", "Select Location")
```
### NotebookOrPlan_1 As label

#### Size


```
=10.5
```
#### Text


```
=If(ShowOneNote, "Notebook", "Plan")
```
### SectionOrBucket_1 As label

#### Size


```
=10.5
```
#### Text


```
=If(ShowOneNote, "Section", "Bucket")
```
### ExportCancel_1 As button

#### OnSelect


```
=Set(ShowOneNote, false);
Set(ShowPlanner, false);
Set(ShowOverlay, false);
Navigate(ExportScreen, None)
```
#### Text


```
=If(TaskSelected, "Delete", "Cancel")
```
### ExportConfirm_1 As button

#### OnSelect


```
=If(ShowOneNote,
    Set(ShowOneNote, false);
    Set(SelectedNoteBook, OneNoteBookSelect_1.SelectedText);
    Set(SelectedSection, SectionsSelect_1.SelectedText);
    Navigate(ExportScreen, None),
   ShowPlanner,
    Set(ShowPlanner, false);
    Set(SelectedPlan, PlannerPlanSelect_1.SelectedText);
    Set(SelectedBucket, PlannerBucketSelect_1.SelectedText);
    Navigate(ExportScreen, None),
   ShowOverlay,
    Set(ShowOverlay, false);
    Set(ExportConfirmed, true);
    Navigate(ConfirmScreen, None)
)

```
#### Text


```
=If(ShowOverlay, "Yes, continue", "OK")
```
### ExportConfirmText_1 As label

#### Size


```
=13.5
```
#### Text


```
="Once you Export, your meeting summary will be shared and you will no longer have access to the edit page."
```
## ExportScreen
  
---
### ExportScreen As screen


Export creation screen
Select where to export to.
Possible exports:
- OneNote
- Office Planner
- Email

#### OnVisible


```
If(IsEmpty(EmailRecipients), 
    ClearCollect(EmailRecipients, AttendeeGallery1.AllItems)
);
If(IsEmpty(OneNoteBooks), ClearCollect(OneNoteBooks,'OneNote(Business)'.GetNotebooks()));
If(!IsEmpty(OneNoteBooks),ClearCollect(OneNoteSections,'OneNote(Business)'.GetSectionsInNotebook(OneNoteBookSelect_1.SelectedText.'data-ADB4D7A662F548B49FAC2B986E348A1BKey').value));
If(IsEmpty(PlannerPlans), ClearCollect(PlannerPlans, Planner.ListMyPlans().value));
If(!IsEmpty(PlannerPlans),ClearCollect(PlannerBuckets,Planner.ListBuckets(PlannerPlanSelect_1.SelectedText.'data-ADB4D7A662F548B49FAC2B986E348A1Bid').value))
```
### ExportMeetingSubject As label

#### Size


```
=12
```
#### Text


```
=SelectedMeeting.Subject
```
### AppLogo7 As image

#### Image


```
='nav-logo'
```
### ExportBannerHeader As label

#### Size


```
=27
```
#### Text


```
="Export " & SelectedMeeting.Subject
```
### ExportQuestion As label

#### Text


```
="Where would you like to export to?"
```
### DataLossWarnText As label

#### Size


```
=10.5
```
#### Text


```
="Unless you select an export location, your meeting notes, attachments, and tasks will be lost once you exit the application."
```
### ExportButton As button

#### OnSelect


```
=Set(ShowOverlay, true);
Navigate(ExportPopUpsScreen, None)
```
#### Text


```
="Export"
```
### ExportIcon As image

#### Image


```
=export
```
#### OnSelect


```
=Select(ExportButton)
```
### OneNoteIcon As image

#### Image


```
='one-note'
```
### OneNoteHeader As label

#### Size


```
=15
```
#### Text


```
="OneNote"
```
### OneNoteExportDescript As label

#### Size


```
=10.5
```
#### Text


```
="Export meeting summary, notes, attachments, and tasks to your OneNote."
```
### ShowOneNoteSelection As button

#### OnSelect


```
=Set(ShowOneNote, true);
Navigate(ExportPopUpsScreen, None);
/*retrieves OneNote sections of (pre)selected OneNote book (if user hasn't selected one yet)*/
ClearCollect(OneNoteSections, 'OneNote(Business)'.GetSectionsInNotebook(OneNoteBookSelect_1.SelectedText.'data-ADB4D7A662F548B49FAC2B986E348A1BKey').value)
```
#### Text


```
=If(ExportToOneNote.Height > 0, "Select new location", "Select Location")
```
### OneNoteDataLossDescript As label

#### Size


```
=9
```
#### Text


```
="Photos and sketches cannot be exported to OneNote. ‘Export to Email’ to prevent attachments from being lost."
```
### OneNoteExportLocation As label

#### Size


```
=10.5
```
#### Text


```
=SelectedNoteBook.Value & " - " & SelectedSection.'data-ADB4D7A662F548B49FAC2B986E348A1Bname'
```
### ExportToOneNote As label

#### Size


```
=10.5
```
#### Text


```
="Export to:"
```
### EmailIcon As image

#### Image


```
=outlook
```
### EmailHeader As label

#### Size


```
=15
```
#### Text


```
="Email"
```
### EmailExportDescript As label

#### Size


```
=10.5
```
#### Text


```
="Email meeting summary, notes, attachments, and tasks to the attendees."
```
### RecipientGalleryBkg As button

#### Text


```
=""
```
### AttendeeCount As label

#### Size


```
=10.5
```
#### Text


```
="Attendees (" & CountRows(EmailRecipients) & ")"
```
### EmailRecipientsGallery As gallery.galleryVertical

#### Items


```
=EmailRecipients
```
### AddAttendee As label

#### Size


```
=10.5
```
#### Text


```
="Add attendee"
```
### AssnTaskSearchUser_1 As text

### UserSearchResults As gallery.galleryVertical

#### Items


```
=If(!IsBlank(AssnTaskSearchUser_1.Text), Office365Users.SearchUser({searchTerm:Trim(AssnTaskSearchUser_1.Text), top:15}))
```
#### OnSelect


```
=If(Not(ThisItem.Id in EmailRecipients.Id), Collect(EmailRecipients, ThisItem))
```
### LoadingIndicator2_1 As label

#### Text


```
="Searching for users..."
```
### PlannerIcon As image

#### Image


```
=planner
```
### OfficePlanner As label

#### Size


```
=15
```
#### Text


```
="Office Planner"
```
### PlannerExportDescript As label

#### Size


```
=10.5
```
#### Text


```
="Sync assigned tasks with Office Planner"
```
### ShowPlannerSelection As button

#### OnSelect


```
=Set(ShowPlanner, true);
Navigate(ExportPopUpsScreen, None)
```
#### Text


```
=If(PlannerExportTo.Height > 0, "Select new location", "Select Location")
```
### PlannerExportLocation As label

#### Size


```
=10.5
```
#### Text


```
=SelectedPlan.'data-ADB4D7A662F548B49FAC2B986E348A1Btitle' & " - " & SelectedBucket.'data-ADB4D7A662F548B49FAC2B986E348A1Bname'
```
### PlannerExportTo As label

#### Size


```
=10.5
```
#### Text


```
="Export to:"
```
## FollowUpScreen
  
---
### FollowUpScreen As screen


Schedule follow up for this meeting
#### OnVisible


```
Set(ExportConfirmed, false);
ClearCollect(FollowUpMeetingAttendees, MeetingAttendees)
```
### AppIcon7 As image

#### Image


```
='nav-logo'
```
### FollowUpHeader As label

#### Size


```
=27
```
#### Text


```
="Schedule a follow up meeting"
```
### FindAvailableTimesButton As button

#### OnSelect


```
=Navigate(FollowUpTimesScreen, None)
```
#### Text


```
="Find Available Times"
```
### FollowUpGallBkg As button

#### Text


```
=""
```
### FollowUpAttendeeCount As label

#### Size


```
=15
```
#### Text


```
="Attendees (" & CountRows(FollowUpMeetingAttendees) & ")"
```
### FollowUpAttendeesGall As gallery.galleryVertical

#### Items


```
=FollowUpMeetingAttendees
```
### AddFollowUpAttendee As label

#### Size


```
=10.5
```
#### Text


```
="Add attendee"
```
### FollowUpSearchText As text

### FollowUpSearchUserResults As gallery.galleryVertical

#### Items


```
=If(!IsBlank(FollowUpSearchText.Text), Office365Users.SearchUser({searchTerm:Trim(FollowUpSearchText.Text), top:15}))
```
#### OnSelect


```
=If(Not(ThisItem.Id in FollowUpMeetingAttendees.Id), Collect(FollowUpMeetingAttendees, ThisItem))
```
### Label16_3 As label

#### Size


```
=15
```
#### Text


```
="Subject"
```
### FollowUpSubject As text

### Label16_4 As label

#### Size


```
=15
```
#### Text


```
="Message"
```
### FollowUpMessage As text

## FollowUpTimesScreen
  
---
### FollowUpTimesScreen As screen


Collections used in galleries and drop downs on this screen
- MeetingDurations
- HoursList

#### OnVisible


```
ClearCollect(MeetingDurations,
{Name:"30 minutes", Minutes:30},{Name:"1 hour", Minutes:60},{Name:"90 minutes", Minutes:90},{Name:"2 hours", Minutes:120},
{Name:"2.5 hours", Minutes:150},{Name:"3 hours", Minutes:180},{Name:"3.5 hours", Minutes:210},{Name:"4 hours", Minutes:240});

ClearCollect(HoursList, {Name:"12:00 am",Minutes:0}, {Name:"12:30 am",Minutes:30}, {Name:"01:00 am",Minutes:60}, {Name:"01:30 am",Minutes:90}, {Name:"02:00 am",Minutes:120}, {Name:"02:30 am",Minutes:150}, {Name:"03:00 am",Minutes:180}, {Name:"03:30 am",Minutes:210}, {Name:"04:00 am",Minutes:240, Short: "4 am"}, {Name:"04:30 am",Minutes:270}, {Name:"05:00 am",Minutes:300}, {Name:"05:30 am",Minutes:330}, {Name:"06:00 am",Minutes:360}, {Name:"06:30 am",Minutes:390}, {Name:"07:00 am",Minutes:420}, {Name:"07:30 am",Minutes:450}, {Name:"08:00 am",Minutes:480, Short: "8 am"}, {Name:"08:30 am",Minutes:510}, {Name:"09:00 am",Minutes:540}, {Name:"09:30 am",Minutes:570}, {Name:"10:00 am",Minutes:600}, {Name:"10:30 am",Minutes:630}, {Name:"11:00 am",Minutes:660}, {Name:"11:30 am",Minutes:690}, {Name:"12:00 pm",Minutes:720, Short: "12 pm"
}, {Name:"12:30 pm",Minutes:750}, {Name:"01:00 pm",Minutes:780}, {Name:"01:30 pm",Minutes:810}, {Name:"02:00 pm",Minutes:840}, {Name:"02:30 pm",Minutes:870}, {Name:"03:00 pm",Minutes:900}, {Name:"03:30 pm",Minutes:930}, {Name:"04:00 pm",Minutes:960, Short: "4 pm"}, {Name:"04:30 pm",Minutes:990}, {Name:"05:00 pm",Minutes:1020}, {Name:"05:30 pm",Minutes:1050}, {Name:"06:00 pm",Minutes:1080}, {Name:"06:30 pm",Minutes:1110}, {Name:"07:00 pm",Minutes:1140}, {Name:"07:30 pm",Minutes:1170}, {Name:"08:00 pm",Minutes:1200, Short: "8 pm"}, {Name:"08:30 pm",Minutes:1230}, {Name:"09:00 pm",Minutes:1260}, {Name:"09:30 pm",Minutes:1290}, {Name:"10:00 pm",Minutes:1320}, {Name:"10:30 pm",Minutes:1350}, {Name:"11:00 pm",Minutes:1380}, {Name:"11:30 pm",Minutes:1410})
```
### AppIcon8 As image

#### Image


```
='nav-logo'
```
### FollowUpTimesHeader As label

#### Size


```
=27
```
#### Text


```
="Schedule a follow up meeting"
```
### SendInvite As button

#### OnSelect


```
=/*creates calendar event for meeting*/
UpdateContext({requiredAttendees:Concat(FollowUpMeetingAttendees, UserPrincipalName & ";")});
UpdateContext({requiredAttendees:Left(requiredAttendees, Len(requiredAttendees)-1)});
Office365Outlook.V4CalendarPostItem(MyCalendarID, FollowUpSubject.Text, FollowUpStart, FollowUpEnd, "UTC",{importance:"Normal", body:FollowUpMessage.Text, showAs:"busy", requiredAttendees:requiredAttendees});
Set(FollowUpConfirmed, true);
Navigate(ConfirmScreen,None)
```
#### Text


```
="Send Invite"
```
### Label20_10 As label

#### Size


```
=15
```
#### Text


```
="Desired date for the meeting"
```
### Label20_12 As label

#### Size


```
=15
```
#### Text


```
="Desired time range"
```
### Label20_13 As label

#### Size


```
=15
```
#### Text


```
="Meeting duration"
```
### LoadAvailableTimes As button

#### OnSelect


```
=Set(Loading, true);
/*
Collects available meeting times for attendees based on user determined data from this page. Adds 'StartTime' and 'EndTime' columns to the collection as a means of simplifying the MeetingTimeSlot column
*/
ClearCollect(MeetingTimes,AddColumns(Office365Outlook.FindMeetingTimes({MaxCandidates:15,MinimumAttendeePercentage: 1, MeetingDuration: MeetingDurationSelection.SelectedText.'data-ADB4D7A662F548B49FAC2B986E348A1BMinutes',Start:Text(DateAdd(DatePicker1.SelectedDate,MeetingStartRange.SelectedText.'data-ADB4D7A662F548B49FAC2B986E348A1BMinutes', Minutes), UTC),End:Text(DateAdd(DatePicker1.SelectedDate, MeetingEndRange.SelectedText.'data-ADB4D7A662F548B49FAC2B986E348A1BMinutes', Minutes), UTC),RequiredAttendees:Concat(FollowUpMeetingAttendees,UserPrincipalName & ";")}).MeetingTimeSuggestions,"StartTime",MeetingTimeSlot.Start.DateTime,
"EndTime",MeetingTimeSlot.End.DateTime));
Set(ShowMeetingTimes, true);
Set(Loading, false)
```
#### Text


```
="Find Available Times"
```
### TimeLine As gallery.galleryHorizontal

#### Items


```
=HoursList
```
### SelectAvailableTime As label

#### Size


```
=15
```
#### Text


```
="Select an available time"
```
### AvailableTimesGall As gallery.galleryVertical

#### Items


```
=SortByColumns(MeetingTimes,"Confidence",Descending,"StartTime",Ascending)
```
### LoadingIndicator3 As label

#### Text


```
="Retrieving available times..."
```
## HomePopUpsScreen
  
---
### HomePopUpsScreen As screen


Gathers and stores the Office 365 profiles of the meeting attendees if they are within the app user's org
#### OnVisible


```
If(IsEmpty(MeetingAttendees),
    Set(Loading, true);
    ClearCollect(MeetingAttendeeEmails, Filter(Split(Concatenate(SelectedMeeting.RequiredAttendees,
     SelectedMeeting.OptionalAttendees), ";"), Result <> ""));
    ClearCollect(MeetingAttendeesTemp, ForAll(MeetingAttendeeEmails, If(Lower(MyDomain) = Lower(Last(Split(Result, "@")).Result), Office365Users.UserProfileV2(Result), {displayName: Result, id: "", image: Blank(), jobTitle: "", userPrincipalName: Result})));
    ClearCollect(MeetingAttendees, RenameColumns(MeetingAttendeesTemp, "id", "Id", "jobTitle", "JobTitle", "displayName", "DisplayName", "userPrincipalName", "UserPrincipalName"));
    Set(SelectedMeetingDuration, DateDiff(SelectedMeeting.Start, SelectedMeeting.End, Seconds));
    Set(Loading, false)
)
```
### AssnTaskHeader_1 As label

#### Size


```
=27
```
#### Text


```
=If(ShowDataLossWarning, "Welcome to your meeting!", "Assign Task")
```
### AssnTaskDescription_1 As text

### AssnTaskDateHeader_1 As label

#### Size


```
=10.5
```
#### Text


```
="Due date"
```
### AssnTaskToHeader_1 As label

#### Size


```
=10.5
```
#### Text


```
="Assign to (your org only)"
```
### AssnTaskGallery_2 As gallery.galleryVertical

#### Items


```
=/*
In-org attendee gallery for task assignment
If the attendee DisplayName is an actual name and not an email address, then they are in the app user's org, so we can assign them a task.
Tasks are stored in an 0365 tenant, so cannot be assigned to external users
*/
Filter(AttendeeGallery1.AllItems, Not(".com" in DisplayName))
```
#### OnSelect


```
=If(AssnTaskGallery_2.Visible,
    Set(UserSelected, true);
    Set(SelectedUser, {DisplayName:AssnTaskGallery_2.Selected.DisplayName, Id:AssnTaskGallery_2.Selected.Id, Image: AssnTaskGallery_2.Selected.AssnTaskUserImg_3.Image, JobTitle:AssnTaskGallery_2.Selected.JobTitle})
)
```
### AssnTaskSearchUser_2 As text

### CancelAssnTask_1 As button

#### OnSelect


```
=Navigate(HomeScreen, None);
Set(ShowOverlay, !ShowOverlay);
If(TaskSelected, RemoveIf(Tasks, Id = SelectedTask.Id));
Set(UserSelected, false);
Set(UserSelectedFromTasks, false);
Set(TaskSelected, false);
Reset(AssnTaskSearchUser_2);
Reset(AssnTaskDueDate_1);
Reset(AssnTaskDescription_1);
Reset(TaskTitle)
```
#### Text


```
=If(TaskSelected, "Delete", "Cancel")
```
### SaveAssnTask_1 As button

#### OnSelect


```
=Navigate(HomeScreen, None);
Set(ShowOverlay, !ShowOverlay);
/*If user is making a new task, collect the information from form, otherwise, revise the task the user is editing*/
If(!TaskSelected,
    Collect(Tasks, {Id: CountRows(Tasks)+1, Name:AssnTaskDescription_1.Text, DueDate: AssnTaskDueDate_1.SelectedDate, 
AssignToUser: SelectedUser}),
    Patch(Tasks, LookUp(Tasks, Id=SelectedTask.Id), {Name:AssnTaskDescription_1.Text, DueDate: AssnTaskDueDate_1.SelectedDate, AssignToUser: SelectedUser}));
Set(UserSelected, false);
Set(UserSelectedFromTasks, false);
Set(TaskSelected, false);
Reset(AssnTaskSearchUser_2);
Reset(AssnTaskDueDate_1);
Reset(AssnTaskDescription_1);
Reset(TaskTitle)
```
#### Text


```
="Save task"
```
### AssnTaskGallery_3 As gallery.galleryVertical

#### Items


```
=/*User search gallery*/
If(!IsBlank(AssnTaskSearchUser_2.Text), Office365Users.SearchUser({searchTerm:Trim(AssnTaskSearchUser_2.Text), top:15}))
```
#### OnSelect


```
=Set(SelectedUser, {DisplayName:AssnTaskGallery_3.Selected.DisplayName, Id:AssnTaskGallery_3.Selected.Id, Image: AssnTaskGallery_3.Selected.AssnTaskUserImg_4.Image, JobTitle:AssnTaskGallery_3.Selected.JobTitle});
Set(UserSelected, true)
```
### LoadingIndicator2_2 As label

#### Text


```
="Searching for users..."
```
### AssnTaskUserImg_5 As image

#### Image


```
=If(UserSelectedFromTasks,SelectedUserTasks.Image,SelectedUser.Image)
```
#### OnSelect


```
=
```
### AssnTaskUserName_5 As label

#### OnSelect


```
=
```
#### Size


```
=8
```
#### Text


```
=If(UserSelectedFromTasks,SelectedUserTasks.DisplayName,SelectedUser.DisplayName)
```
### AssnTaskUserJob_5 As label

#### OnSelect


```
=
```
#### Size


```
=8
```
#### Text


```
=If(UserSelectedFromTasks,SelectedUserTasks.JobTitle,SelectedUser.JobTitle)
```
### DataWarningAccept_1 As button

#### OnSelect


```
=Set(ShowDataLossWarning, false);
Navigate(HomeScreen, None)
```
#### Text


```
="Got it!"
```
### OrgAttendees_1 As label

#### Text


```
="No attendees in your org"
```
## HomeScreen
  
---
### HomeScreen As screen


The main screen for meeting captures during a meeting.

- create meeting notes
- create tasks
- see meeting details

#### OnVisible


```
/*if any additional meeting is captured in the same session, guarantees no confirmation screens are shown in error*/
Set(FollowUpConfirmed, false);
Set(EmailConfirmed, false);
Set(ExportConfirmed, false)
```
### AppLogo1 As image

#### Image


```
='nav-logo'
```
### NavHome1 As image

#### Image


```
='nav-notes'
```
### NavSketch1 As image

#### Image


```
='nav-sketch'
```
#### OnSelect


```
=Navigate(SketchScreen, None)
```
### NavPhotos1 As image

#### Image


```
='nav-camera'
```
#### OnSelect


```
=Navigate(CameraScreen, None)
```
### AttendeesBanner As label

#### Size


```
=10.5
```
#### Text


```
="Attendees"
```
### AttendeesBannerImage As image

#### Image


```
=attendees
```
### AttendeeGallery1 As gallery.galleryVertical

#### Items


```
=MeetingAttendees
```
### LoadingIndicator1 As label

#### Size


```
=10
```
#### Text


```
="Gathering meeting attendees..."
```
### MailAllButton As button

#### OnSelect


```
=Navigate(EmailScreen, None);
Set(MultiRecipients, true);
ClearCollect(EmailRecipients, AttendeeGallery1.AllItems)
```
#### Text


```
="Email"
```
### NotesBanner As label

#### Size


```
=10.5
```
#### Text


```
="Notes"
```
### NotesIcon As image

#### Image


```
=notes
```
### NotesInput As text

### DetailsBanner As label

#### Text


```
="Meeting Details"
```
### MeetingTitle As label

#### Size


```
=15
```
#### Text


```
=SelectedMeeting.Subject
```
### HomeTimeRange As label

#### Size


```
=10.5
```
#### Text


```
=Text(SelectedMeeting.Start,"[$-en-US]mmmm dd, yyyy")&" | " & Lower(Text(SelectedMeeting.Start,"[$-en-US]hh:mm am/pm"))&" - "&Lower(Text(SelectedMeeting.End,"[$-en-US]hh:mm am/pm")) & " (" & DateDiff(SelectedMeeting.Start, SelectedMeeting.End, Minutes) & " minutes)"
```
### Finish_SaveButton As button

#### OnSelect


```
=Navigate(ExportScreen, None)
```
#### Text


```
="Finish & Save"
```
### Finish_SaveIcon As image

#### Image


```
=export
```
#### OnSelect


```
=Select(Finish_SaveButton)
```
### TasksBanner As label

#### Size


```
=10.5
```
#### Text


```
="Planner Tasks"
```
### TasksIcon As image

#### Image


```
=tasks
```
### TaskGallery As gallery.galleryVertical

#### Items


```
=Tasks
```
#### OnSelect


```
=If(CountRows(Tasks) > 0, 
Set(SelectedTask, ThisItem);
Set(TaskSelected, true);
Set(UserSelected, true);
Set(UserSelectedFromTasks, true);
Set(SelectedUserTasks, ThisItem.AssignToUser);
Set(ShowOverlay, true)
)
```
### TaskTitle As text

### InitialTaskCount As label

#### Size


```
=10.5
```
#### Text


```
="0 tasks"
```
## SketchScreen
  
---
### SketchScreen As screen


Create a sketch during a meeting.
#### OnVisible


```
Set(ShowSketchSaved, false)
```
### AppLogo2 As image

#### Image


```
='nav-logo'
```
### NavHome2 As image

#### Image


```
='nav-notes'
```
#### OnSelect


```
=Navigate(HomeScreen, None)
```
### NavSketch2 As image

#### Image


```
='nav-sketch'
```
### NavPhotos2 As image

#### Image


```
='nav-camera'
```
#### OnSelect


```
=Navigate(CameraScreen, None)
```
### SaveSketch As button

#### OnSelect


```
=/*store sketches in sketch collection*/
Set(SketchNumber, SketchNumber + 1);
Collect(Sketches, {Image:SketchCanvas.Image, Name: "Sketch" & SketchNumber & ".jpg"});
Reset(SketchCanvas);
Set(ShowSketchSaved, true)
```
#### Text


```
="Save sketch"
```
### SavedIndicator As label

#### Size


```
=12
```
#### Text


```
="Saved!"
```
## WelcomeScreen
  
---
### WelcomeScreen As screen


if any additional meeting is captured in the same session, guarantees all collections are empty
#### OnVisible


```
Clear(MeetingAttendees);
Clear(MeetingTimes);
Clear(EmailRecipients);
Clear(FollowUpMeetingAttendees);
Clear(Tasks);
Clear(Photos);
Clear(Sketches);
Clear(EmailAttachments);
Reset(NotesInput);
Reset(AssnTaskSearchUser_1);
Set(FollowUpConfirmed, false);
Set(EmailConfirmed, false);
Set(ExportConfirmed, false);

/*Email and OneNote templates with {placeholder} values for dynamic information*/

ClearCollect(Templates,
{Template: "Email", Value: "<!DOCTYPE html><html><head><title>" & "{MeetingName}" & "</title><style>div{box-sizing:border-box}table{table-layout:fixed;background-color:#eaedef;width:829px;font-family:'Open Sans',sans-serif;color:#2c3034}table.with-border td{border:2px solid #e3e3e3;background-color:#fff;vertical-align:top}td.caption{height:65px;background:#ed2955;color:#fff;text-align:center;vertical-align:middle}.details{font-size:14px;color:#2c3034;padding-top:10px}.header{font-size:16px;font-weight:600}.mark{font-weight:400;color:#617281}.name{font-size:12px;font-weight:600;color:#ed2955}table.no-border td.user-name{font-size:14px;font-weight:600;color:#2c3034;vertical-align:middle;height:20px;}.due-time{text-align:right;font-size:10px;vertical-align:middle;color:#617281;font-weight:400}.assign-to{font-size:12px;color:#617281}.job-title{font-size:12px;color:#4a4a4a;height:20px}table.no-border{width:100%}table.no-border td{border:0}table.no-border td.task{padding:10px 0;border-top:1px solid #f1f1f1}.user-img img{width:17px;height:19px;border:0;}.name a.link-name,.name a.link-name:visited{color:#ed2955;text-decoration:none;}</style></head><body><table border='0' cellpadding='0' cellspacing='0'><tr><td class='caption'>[ Meeting Capture ]</td></tr><tr><td style='border: 0;background-color: #eaedef;padding:30px 0 0 0;text-align: center;color: #2c3034;font-size: 20px;font-weight: 600;'>" & "{MeetingName}" & "</td></tr><tr><td style='border: 0;background-color: #eaedef;padding: 9px 0 10px 0;text-align: center;color: #2c3034;font-size: 14px;'>" & "{MeetingStartDate}" &" | " & "{MeetingStartTime}" & " - "& "{MeetingEndTime}" & " (" & "{MeetingMinutes}" & " Minutes)</td></tr></table><table class='with-border' border='0' cellpadding='20' cellspacing='20'><tr>
<td colspan='2' style='padding-bottom:10px;'><table border='0' cellpadding='0' cellspacing='0' class='no-border' style='table-layout:auto;'><tr><td colspan='3' class='header'>Attendees <span class='mark'>(" & "{MeetingAttendeeNum}" & ")</span></td></tr><tr><td colspan='3' style='height:10px;'></td></tr>" & "{1}" & "</table></td></tr><tr><td colspan='2'><table border='0' cellpadding='0' cellspacing='0' class='no-border'><tr><td class='header'>Meeting details</td></tr><tr><td class='details'>" & "{MeetingDetails}" & "</td></tr></table></td></tr><tr><td width='50%'><table border='0' cellpadding='0' cellspacing='0' class='no-border'><tr><td class='header'>Meeting Notes</td></tr><tr><td class='details'>" & "{MeetingNotes}" & "</td></tr></table></td><td width='50%'><table border='0' cellpadding='0' cellspacing='0' class='no-border'><tr><td class='header' style='padding-bottom:10px;'>Tasks</td></tr>" & "{2}" & "</table></td></tr><tr><td style='border:0;background-color:#eaedef;padding:0;height:10px;'></td></tr></table></body></html>"},
{Template: "OneNote", Value: "<!DOCTYPE html><html><head><title>" & "{MeetingName}" & "</title><meta http-equiv='Content-Type' content='text/html; charset=utf-8'/></head><body data-absolute-enabled='true' style='font-family:Calibri;font-size:11pt'><div data-id='_default' style='position:absolute;left:48px;top:120px;width:829px;'><table border='0' cellpadding='0' cellspacing='0' width='829'><tr><td style='background-color:#ed2955;font-size:10pt;'>&nbsp;</td></tr><tr><td style='background-color:#ed2955;border:0px;text-align:center;font-weight:600;'><span style='color:white'>[ Meeting Capture ]</span></td></tr><tr><td style='background-color:#ed2955;font-size:8pt;'>&nbsp;</td></tr><tr><td style='background-color:#eaedef;font-size:14pt;'>&nbsp;</td></tr><tr><td style='background-color:#eaedef;border:0px;text-align:center;'><span style='font-size:15pt;color:#2c3034;font-weight:bold'>" & "{MeetingName}" & "</span></td></tr><tr><td style='background-color:#eaedef;border:0px;text-align:center;'><span style='font-size:10.5pt;color:#2c3034'>" & "{MeetingStartDate}" &" | " & "{MeetingStartTime}"&" - "& "{MeetingEndTime}" & " (" & "{MeetingMinutes}" & " Minutes)</span></td></tr><tr><td style='background-color:#eaedef;font-size:14pt;'>&nbsp;</td></tr><tr><td style='background-color:white;'><table border='0' cellpadding='0' cellspacing='0' width='829'><colgroup><col style='width: 210px;'><col style='width: 210px;'><col style='width: 210px;'><col style='width: 210px;'></colgroup><tr><td colspan='4' style='font-size:14pt;'><span style='font-weight:600;color:#2c3034'>Attendees</span>&nbsp;<span style='color:#617281'>(" & "{MeetingAttendeeNum}" & ")</span></td></tr>" & "{1}" & "</table></td></tr><tr><td style='background-color:#ffffff;font-size:8pt;'>&nbsp;</td></tr><tr><td style='background-color:#ffffff;font-size:8pt;'>&nbsp;</td></tr><tr><td style='background-color:white;'><table border='0' cellpadding='0' cellspacing='0' width='829'><tr><td width='420' style='font-size:14pt;font-weight:600;color:#2c3034'>Meeting Notes</td><td width='420' style='font-size:14pt;font-weight:600;color:#2c3034;border:10px solid red;'>Tasks</td></tr><tr><td style='font-size:12pt;color:#2c3034'>" & "{MeetingNotes}" & "</td><td style='font-size:14pt;font-weight:600;color:#2c3034'><table border='0' cellpadding='0' cellspacing='0' width='420'>" & "{2}" & "</table></td></tr></table></td></tr><tr><td style='background-color:#ffffff;font-size:8pt;'>&nbsp;</td></tr><tr><td style='background-color:white;'></td></tr><tr><td style='background-color:#eaedef;font-size:26.5pt;'>&nbsp;</td></tr></table></div></body></html>"})
```
### MeetingsGalleryBkg As button

#### OnSelect


```
=Select(Parent)
```
#### Text


```
=""
```
### LblMeetTitle As label

#### OnSelect


```
=Select(Parent)
```
#### Text


```
=ThisItem.Subject
```
### LblStart_End As label

#### OnSelect


```
=Select(Parent)
```
#### Text


```
=Lower(Text(ThisItem.Start,"[$-en-US]hh:mm am/pm"))&" - "&Lower(Text(ThisItem.End,"[$-en-US]hh:mm am/pm"))&" |  "&ThisItem.Location
```
### BtnChangeAuto As button

#### OnSelect


```
=Set(AutoSelectMeeting, false)
```
#### Text


```
="Change"
```