<!DOCTYPE html>
<html>
***REMOVED***<head>
***REMOVED***<link rel="stylesheet" href="main.css">
***REMOVED***<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
***REMOVED***<script>
***REMOVED******REMOVED***var paramsObject;
***REMOVED******REMOVED***let events_JSON;


***REMOVED******REMOVED***function get_splotlight_content() {
***REMOVED******REMOVED***var return_value = "";

***REMOVED******REMOVED***var start = new Date(events_JSON[0].start);
***REMOVED******REMOVED***var start_date = start.toLocaleString('en-AU', {weekday: "long", day: "numeric", month: "long", year: "numeric"});
***REMOVED******REMOVED***var start_time = start.toLocaleString('en-AU', {hour: "numeric", minute: "numeric", hourCycle: "h12"});

***REMOVED******REMOVED***var content_container_classes = "";
***REMOVED******REMOVED***var main_content_classes = "";
***REMOVED******REMOVED***var details_content_classes = "";
***REMOVED******REMOVED***var subdetails_content_classes = "";

***REMOVED******REMOVED***switch (paramsObject.Display) {
***REMOVED******REMOVED******REMOVED***case "Portrait":
***REMOVED******REMOVED******REMOVED***content_container_classes = "rows";
***REMOVED******REMOVED******REMOVED***main_content_classes = "rows middle h65 w90";
***REMOVED******REMOVED******REMOVED***details_content_classes = "columns h25 w90";
***REMOVED******REMOVED******REMOVED***subdetails_content_classes = "";
***REMOVED******REMOVED******REMOVED***break;
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***case "Square":
***REMOVED******REMOVED******REMOVED***content_container_classes = "rows";
***REMOVED******REMOVED******REMOVED***main_content_classes = "rows middle h45 w90";
***REMOVED******REMOVED******REMOVED***details_content_classes = "columns h45 w90";
***REMOVED******REMOVED******REMOVED***subdetails_content_classes = "";
***REMOVED******REMOVED******REMOVED***break;
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***case "Footer":
***REMOVED******REMOVED******REMOVED***content_container_classes = "rows";
***REMOVED******REMOVED******REMOVED***main_content_classes = "rows middle h65 w65";
***REMOVED******REMOVED******REMOVED***details_content_classes = "columns h25 w65";
***REMOVED******REMOVED******REMOVED***subdetails_content_classes = "";
***REMOVED******REMOVED******REMOVED***break;
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***case "Landscape":
***REMOVED******REMOVED******REMOVED***content_container_classes = "columns";
***REMOVED******REMOVED******REMOVED***main_content_classes = "rows middle w65 h90";
***REMOVED******REMOVED******REMOVED***details_content_classes = "rows w25 h90";
***REMOVED******REMOVED******REMOVED***subdetails_content_classes = "rows middle h65";
***REMOVED******REMOVED******REMOVED***break;
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***default:
***REMOVED******REMOVED******REMOVED***break;
***REMOVED******REMOVED***

***REMOVED******REMOVED***return_value += "<div class='" + content_container_classes + "'>";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + main_content_classes + "'>";

***REMOVED******REMOVED******REMOVED***return_value += "<h1 class='heading_text'>" + events_JSON[0].name + "</h1>";
***REMOVED******REMOVED******REMOVED***return_value += "<h2 class='subheading_text'>" + events_JSON[0].summary + "</h2>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + details_content_classes + "'>";

***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + subdetails_content_classes + "'>";

***REMOVED******REMOVED******REMOVED******REMOVED***if (paramsObject.Display == "Footer") {
***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h3 class='details_text'>" + start_date + " | " + start_time + "</h3>";
***REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h3 class='details_text'>" + start_date + "</h3>";
***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h3 class='details_text'>" + start_time + "</h3>";
***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h3 class='details_text'>" + (events_JSON[0].venue.search(/https/) == -1 ? events_JSON[0].venue : "Online") + "</h3>";
***REMOVED******REMOVED******REMOVED***

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED******REMOVED***return_value += "<div>";

***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<img src='https://quickchart.io/qr?text=https://unihub.qut.edu.au/students/events/Detail/" + events_JSON[0].entityId + "' class='QR_code'></img>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED***return return_value;
***REMOVED***

***REMOVED******REMOVED***function get_summary_content() {
***REMOVED******REMOVED***var return_value = "";

***REMOVED******REMOVED***events_JSON.forEach(e => {
***REMOVED******REMOVED******REMOVED***var start = new Date(e.start);
***REMOVED******REMOVED******REMOVED***// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString
***REMOVED******REMOVED******REMOVED***var start_date = start.toLocaleString('en-AU', {weekday: "long", day: "numeric", month: "long", year: "numeric"});
***REMOVED******REMOVED******REMOVED***var start_time = start.toLocaleString('en-AU', {hour: "numeric", minute: "numeric", hourCycle: "h12"});

***REMOVED******REMOVED******REMOVED***var content_container_classes = "rows distribute";
***REMOVED******REMOVED******REMOVED***var main_content_classes = "rows middle h12 w90";
***REMOVED******REMOVED******REMOVED***var details_content_classes = "columns h6 w90";

***REMOVED******REMOVED******REMOVED***if (paramsObject.Display == "Landscape") {
***REMOVED******REMOVED******REMOVED***main_content_classes = "rows middle h12";
***REMOVED******REMOVED******REMOVED***details_content_classes = "columns h6";
***REMOVED******REMOVED*** 

***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + content_container_classes + "'>";
***REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + main_content_classes + "'>";

***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h1 class='heading_text'>" + e.name + "</h1>";
***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h2 class='subheading_text'>" + e.summary + "</h2>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + details_content_classes + "'>";

***REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h3 class='details_text'>" + start_date + " | " + start_time + "</h3>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";
***REMOVED******REMOVED***);

***REMOVED******REMOVED***return return_value;
***REMOVED***

***REMOVED******REMOVED***function get_list_content() {
***REMOVED******REMOVED***var return_value = "";

***REMOVED******REMOVED***var dates = [];

***REMOVED******REMOVED***events_JSON.forEach(e => {
***REMOVED******REMOVED******REMOVED***var start = new Date(e.start);
***REMOVED******REMOVED******REMOVED***var start_date = start.toLocaleString('en-AU', {weekday: "long", day: "numeric", month: "long", year: "numeric"});

***REMOVED******REMOVED******REMOVED***if (!dates.includes(start_date)) dates.push(start_date);
***REMOVED******REMOVED***);

***REMOVED******REMOVED***var content_container_classes = "rows spacing_needed";
***REMOVED******REMOVED***var main_content_classes = "rows w90";
***REMOVED******REMOVED***var details_content_classes = "columns h6 w90 lp1";

***REMOVED******REMOVED***if (paramsObject.Display == "Landscape") {
***REMOVED******REMOVED******REMOVED***main_content_classes = "rows";
***REMOVED******REMOVED******REMOVED***details_content_classes = "columns h6 lp1";
***REMOVED******REMOVED*** 

***REMOVED******REMOVED***dates.forEach(d => {
***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + content_container_classes + "'>";
***REMOVED******REMOVED******REMOVED***return_value += "<h1 class='heading_text'>" + d + "</h1>";
***REMOVED******REMOVED******REMOVED***return_value += "<div class='system-line'></div>";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return_value += "<div class='" + main_content_classes + "'>";

***REMOVED******REMOVED******REMOVED******REMOVED***events_JSON.forEach(e => {
***REMOVED******REMOVED******REMOVED******REMOVED***var start = new Date(e.start);
***REMOVED******REMOVED******REMOVED******REMOVED***var start_date = start.toLocaleString('en-AU', {weekday: "long", day: "numeric", month: "long", year: "numeric"});
***REMOVED******REMOVED******REMOVED******REMOVED***var start_time = start.toLocaleString('en-AU', {hour: "numeric", minute: "numeric", hourCycle: "h12"});

***REMOVED******REMOVED******REMOVED******REMOVED***if (start_date == d) {
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<div class='" + details_content_classes + "'>";

***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h3 class='details_text padding_override w15'>" + start_time + "</h3>";
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<h2 class='heading_text w75'>" + e.name + "</h2>";

***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***return_value += "<div class='system-line'></div>";
***REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***);

***REMOVED******REMOVED******REMOVED***return_value += "</div>";

***REMOVED******REMOVED******REMOVED***return_value += "</div>";
***REMOVED******REMOVED***)

***REMOVED******REMOVED***return return_value;
***REMOVED***

***REMOVED******REMOVED***function create_content() {
***REMOVED******REMOVED***if (paramsObject.Debug) {
***REMOVED******REMOVED******REMOVED***document.documentElement.style.setProperty('--background-outside', "antiquewhite");
***REMOVED******REMOVED******REMOVED***document.documentElement.style.setProperty('--background-inside', "cadetblue");
***REMOVED******REMOVED***

***REMOVED******REMOVED***if (paramsObject.TextCol) {
***REMOVED******REMOVED******REMOVED***document.documentElement.style.setProperty('--textCol', ('#' + paramsObject.TextCol));
***REMOVED******REMOVED***
***REMOVED******REMOVED***if (paramsObject.LineCol) {
***REMOVED******REMOVED******REMOVED***document.documentElement.style.setProperty('--lineCol', ('#' + paramsObject.LineCol));
***REMOVED******REMOVED***

***REMOVED******REMOVED***var HTML_output = "<div class='output_container'>";

***REMOVED******REMOVED***if (parseInt(paramsObject.ShowEvent) == 1 && events_JSON.length > 0) {
***REMOVED******REMOVED******REMOVED***HTML_output += get_splotlight_content();

***REMOVED******REMOVED*** else if (parseInt(paramsObject.ShowEvent) < 6 && events_JSON.length > 0) {
***REMOVED******REMOVED******REMOVED***if (paramsObject.Display == "Footer") {
***REMOVED******REMOVED******REMOVED***HTML_output += get_splotlight_content();

***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***if (paramsObject.Display == "Landscape"){
***REMOVED******REMOVED******REMOVED******REMOVED***HTML_output = "<div class='output_container width_restrict'>";
***REMOVED******REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").style.flexDirection = "row-reverse";
***REMOVED******REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").style.justifyContent = "flex-start";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***HTML_output += get_summary_content();

***REMOVED******REMOVED***
***REMOVED******REMOVED*** else if (events_JSON.length > 0) {
***REMOVED******REMOVED******REMOVED***if (paramsObject.Display == "Landscape"){
***REMOVED******REMOVED******REMOVED***HTML_output = "<div class='output_container width_restrict'>";
***REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").style.flexDirection = "row-reverse";
***REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").style.justifyContent = "flex-start";
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***HTML_output += get_list_content();
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***HTML_output += "No upcomming events.";
***REMOVED******REMOVED***

***REMOVED******REMOVED***HTML_output += "</div>";
***REMOVED******REMOVED***document.getElementById("output_wrapper").innerHTML = HTML_output;

***REMOVED******REMOVED***if (paramsObject.QR == "N") document.documentElement.style.setProperty('--qrVisible', 'hidden');
***REMOVED***

***REMOVED******REMOVED***function fetch_events() {
***REMOVED******REMOVED***if (paramsObject['ID'].length > 0 || paramsObject['Query'].length > 0) {
***REMOVED******REMOVED******REMOVED***paramsObject['Days'] = 365;
***REMOVED******REMOVED***

***REMOVED******REMOVED***const params = new URLSearchParams(paramsObject);

***REMOVED******REMOVED***fetch('fetch-events.php' + '?' + params.toString())
***REMOVED******REMOVED******REMOVED***.then(response => {
***REMOVED******REMOVED******REMOVED***if (!response.ok) {
***REMOVED******REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").innerHTML = "<div class='output_container'>An error was encountered when fetching the event data.</div>";
***REMOVED******REMOVED******REMOVED******REMOVED***throw new Error('Network response was not ok');
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return response.text();
***REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED***.then(htmlContent => {
***REMOVED******REMOVED******REMOVED***events_JSON = JSON.parse(htmlContent);
***REMOVED******REMOVED******REMOVED***console.log(events_JSON);
***REMOVED******REMOVED******REMOVED***create_content();
***REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED***.catch(error => {
***REMOVED******REMOVED******REMOVED***console.error('There was a problem with the fetch operation:', error);
***REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").innerHTML = "<div class='output_container'>An error was encountered when processing the event data.</div>";
***REMOVED******REMOVED***);
***REMOVED***

***REMOVED******REMOVED***function input_vs_output() {
***REMOVED******REMOVED***const queryString = window.location.search;
***REMOVED******REMOVED***const urlParams = new URLSearchParams(queryString);
***REMOVED******REMOVED***paramsObject = Object.fromEntries(urlParams.entries());

***REMOVED******REMOVED***console.log(paramsObject);

***REMOVED******REMOVED***if (urlParams.size == 0) {
***REMOVED******REMOVED******REMOVED***document.getElementById("output_wrapper").style.display = "none";
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***document.getElementById("input_wrapper").style.display = "none";
***REMOVED******REMOVED******REMOVED***fetch_events();
***REMOVED******REMOVED***
***REMOVED***

***REMOVED******REMOVED***document.addEventListener('DOMContentLoaded', input_vs_output);
***REMOVED***</script>
***REMOVED***</head>
***REMOVED***<body>
***REMOVED***<div id="input_wrapper" class="wrapper">
***REMOVED******REMOVED***<div class="input_container">
***REMOVED******REMOVED***<form class="form_">
***REMOVED******REMOVED******REMOVED***<div class="form_row">
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-4 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Query">Query:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="text" id="Query" name="Query"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-4 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Skip">Skip:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="number" id="Skip" name="Skip" value="0"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-4 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="ID">Filter ID:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="number" id="ID" name="ID"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>

***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***<div class="form_row">
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="CampusIs">Location - Campus:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<select name="CampusIs" id="CampusIs">
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="">Any</option>
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="GP">Gardens Point</option>
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="KG">Kelvin Grove</option>
***REMOVED******REMOVED******REMOVED******REMOVED***</select>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="BlockIs">Location - Block:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="text" id="BlockIs" name="BlockIs"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="LevelIs">Location - Level:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="number" id="LevelIs" name="LevelIs"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="RoomIs">Location - Room:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="number" id="RoomIs" name="RoomIs"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>

***REMOVED******REMOVED******REMOVED***<div class="form_row">
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Campus">Show - Campus:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<div style="display: flex; flex-direction: row; gap: 30px;">
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input type="radio" id="Campus_Yes" name="Campus" value="Y">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="Y">Y</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input checked type="radio" id="Campus_No" name="Campus" value="N">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="N">N</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Block">Show - Block:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<div style="display: flex; flex-direction: row; gap: 30px;">
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input type="radio" id="Block_Yes" name="Block" value="Y">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="Y">Y</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input checked type="radio" id="Block_No" name="Block" value="N">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="N">N</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Level">Show - Level:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<div style="display: flex; flex-direction: row; gap: 30px;">
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input type="radio" id="Level_Yes" name="Level" value="Y">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="Y">Y</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input checked type="radio" id="Level_No" name="Level" value="N">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="N">N</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Room">Show - Room:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<div style="display: flex; flex-direction: row; gap: 30px;">
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input type="radio" id="Room_Yes" name="Room" value="Y">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="Y">Y</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input checked type="radio" id="Room_No" name="Room" value="N">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="N">N</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>

***REMOVED******REMOVED******REMOVED***<div class="form_row">
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="ShowEvent">Number of Events:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="number" id="ShowEvent" name="ShowEvent" value=""><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Days">Days:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="number" id="Days" name="Days" value=""><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Price">Show - Price:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<div style="display: flex; flex-direction: row; gap: 30px;">
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input type="radio" id="Price_Yes" name="Price" value="Y">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="Y">Y</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input checked type="radio" id="Price_No" name="Price" value="N">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="N">N</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="QR">Show - QR Code:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<div style="display: flex; flex-direction: row; gap: 30px;">
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input type="radio" id="QR_Yes" name="QR" value="Y">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="Y">Y</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<input checked type="radio" id="QR_No" name="QR" value="N">
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<label for="N">N</label>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>

***REMOVED******REMOVED******REMOVED***<div class="form_row">
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="TextCol">Text Colour:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="text" id="TextCol" name="TextCol"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="LineCol">Line Colour:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<input type="text" id="LineCol" name="LineCol"><br>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***<div class="col-xs-12 col-sm-4 col-md-3 col-lg-3">
***REMOVED******REMOVED******REMOVED******REMOVED***<label for="Display">Display Layout:</label><br>
***REMOVED******REMOVED******REMOVED******REMOVED***<select name="Display" id="Display">
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="Portrait">Portrait</option>
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="Square">Square</option>
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="Footer">Footer</option>
***REMOVED******REMOVED******REMOVED******REMOVED***<option value="Landscape">Landscape</option>
***REMOVED******REMOVED******REMOVED******REMOVED***</select>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</div>

***REMOVED******REMOVED******REMOVED***<button type="submit" onclick="submitform()">Select Parameters</button>
***REMOVED******REMOVED***</form>
***REMOVED******REMOVED***</div>
***REMOVED***</div>

***REMOVED***<div id="output_wrapper" class="wrapper">
***REMOVED******REMOVED***
***REMOVED***</div>
***REMOVED***</body>
</html>