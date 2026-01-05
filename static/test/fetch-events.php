***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***



***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***curl_setopt($ch, CURLOPT_URL, $authorization_url);
***REMOVED***curl_setopt($ch, CURLOPT_POST,1);
***REMOVED***curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
***REMOVED***curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
***REMOVED***curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
***REMOVED***curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
***REMOVED***curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

***REMOVED***$response = curl_exec($ch);
***REMOVED***curl_close($ch);

***REMOVED***$response = json_decode($response, true);
***REMOVED***$access_token = $response['access_token'];

***REMOVED***return $access_token;
***REMOVED***
***REMOVED***
***REMOVED***function update_event_data_cache(){
***REMOVED***global $filename;
***REMOVED***global $ID;
***REMOVED***global $Days;

***REMOVED***$take = 50;
***REMOVED***$parsed_results = 0;
***REMOVED***$number_of_results = $take;

***REMOVED***$all_events = [];

***REMOVED***$access_token = get_access_token();

***REMOVED***while ($number_of_results === $take) {
***REMOVED******REMOVED***$baseURL = "https://unihub.qut.edu.au/api/integrations/v1/events/current";
***REMOVED******REMOVED***$urlParams = [
***REMOVED******REMOVED***"take"  => $take,
***REMOVED******REMOVED***"skip"  => $parsed_results,
***REMOVED******REMOVED***"sortOptions.order" => "Start",
***REMOVED******REMOVED***"sortOptions.descending" => "false"
***REMOVED******REMOVED***

***REMOVED******REMOVED***if (strlen($ID) > 0) {
***REMOVED******REMOVED***$urlParams["filterOptions.filterIds"] = $ID;
***REMOVED******REMOVED***$urlParams["filterOptions.filterOperator"] = "And";
***REMOVED******REMOVED***
***REMOVED******REMOVED***
***REMOVED******REMOVED***$day = new DateInterval("P1D");
***REMOVED******REMOVED***$now->sub($day);

***REMOVED******REMOVED***$later = new DateTime();
***REMOVED******REMOVED***$month = new DateInterval("P1M");
***REMOVED******REMOVED***$later->add($month);

***REMOVED******REMOVED***$urlParams["dateOptions.from"] = $now->format("Y-m-d\Th\:i\:s\Z");
***REMOVED******REMOVED***$urlParams["dateOptions.to"] = $later->format("Y-m-d\Th\:i\:s\Z");
***REMOVED******REMOVED***$urlParams["dateOptions.date"] = "Start";
***REMOVED***

***REMOVED******REMOVED***$fullURL = $baseURL ."?". http_build_query($urlParams);

***REMOVED******REMOVED***$curl = curl_init();
***REMOVED******REMOVED***curl_setopt($curl, CURLOPT_URL, $fullURL);
***REMOVED******REMOVED***curl_setopt($curl, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
***REMOVED******REMOVED***curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
***REMOVED******REMOVED***curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);
***REMOVED******REMOVED***curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
***REMOVED******REMOVED***curl_setopt($curl, CURLOPT_HTTPHEADER, [
***REMOVED******REMOVED***'accept: application/json',
***REMOVED******REMOVED***'authorization: Bearer ' . $access_token
***REMOVED******REMOVED***]);


***REMOVED******REMOVED***$response = curl_exec($curl);
***REMOVED******REMOVED***curl_close($curl);

***REMOVED******REMOVED***$response = json_decode($response, true);

***REMOVED******REMOVED***foreach ($response as $event) {
***REMOVED******REMOVED***array_push($all_events, json_encode($event, JSON_PRETTY_PRINT));
***REMOVED***

***REMOVED******REMOVED***$number_of_results = count($response);
***REMOVED******REMOVED***$parsed_results += $number_of_results;
***REMOVED***
***REMOVED***file_put_contents($filename, '[' . implode(",", $all_events) . ']');
***REMOVED***


***REMOVED***
***REMOVED***function get_results_by_params() {
***REMOVED***global $filename;
***REMOVED***global $Days;

***REMOVED***$Query = "";
***REMOVED***$Skip = "";
***REMOVED***$CampusIs = "";
***REMOVED***$BlockIs = "";
***REMOVED***$LevelIs = "";
***REMOVED***$RoomIs = "";
***REMOVED***$ShowEvent = "";

***REMOVED***isset($_GET['Query']) ? $Query = $_GET['Query'] : $Query = "";
***REMOVED***isset($_GET['Skip']) && strlen($_GET['Skip']) > 0 ? $Skip = (int) $_GET['Skip'] : $Skip = 0;
***REMOVED***isset($_GET['CampusIs']) ? $CampusIs = $_GET['CampusIs'] : $CampusIs = "";
***REMOVED***isset($_GET['BlockIs']) ? $BlockIs = $_GET['BlockIs'] : $BlockIs = "";
***REMOVED***isset($_GET['LevelIs']) ? $LevelIs = $_GET['LevelIs'] : $LevelIs = "";
***REMOVED***isset($_GET['RoomIs']) ? $RoomIs = $_GET['RoomIs'] : $RoomIs = "";
***REMOVED***isset($_GET['ShowEvent']) && strlen($_GET['ShowEvent']) > 0 ? $ShowEvent = (int) $_GET['ShowEvent'] : $ShowEvent = 10;

***REMOVED***$fileContents = file_get_contents($filename);
***REMOVED***$all_events_JSON = json_decode($fileContents, true);

***REMOVED***// echo json_encode($all_events_JSON, JSON_PRETTY_PRINT);

***REMOVED***$query_filtered_events_JSON = [];
***REMOVED***$room_filter_value = "";
***REMOVED***if (strlen($CampusIs) > 0) {
***REMOVED******REMOVED***$room_filter_value = $room_filter_value . $CampusIs . "-";
***REMOVED***
***REMOVED***if (strlen($BlockIs) > 0) {
***REMOVED******REMOVED***$room_filter_value = $room_filter_value . $BlockIs . "-";
***REMOVED***
***REMOVED***if (strlen($RoomIs) > 0) {
***REMOVED******REMOVED***$room_filter_value = $room_filter_value . $RoomIs;
***REMOVED*** else if (strlen($LevelIs) > 0) {
***REMOVED******REMOVED***$room_filter_value = $room_filter_value . $LevelIs;
***REMOVED***

***REMOVED***foreach ($all_events_JSON as $event) {
***REMOVED******REMOVED***if ((str_contains($event["details"], $Query) || str_contains($event["name"], $Query)) && str_contains($event["location"], $room_filter_value)) {
***REMOVED******REMOVED***array_push( $query_filtered_events_JSON, $event );
***REMOVED***
***REMOVED***
***REMOVED***// echo json_encode($query_filtered_events_JSON, JSON_PRETTY_PRINT);

***REMOVED***$time_filtered_events_JSON = [];
***REMOVED***$utcTimeZone = new DateTimeZone('+1000');
***REMOVED***$now_time = new DateTime('now', $utcTimeZone);

***REMOVED***foreach ($query_filtered_events_JSON as $event) {***REMOVED*** 
***REMOVED******REMOVED***$event_start = new DateTime($event["start"]);
***REMOVED******REMOVED***$interval = $event_start->diff($now_time);

***REMOVED******REMOVED***if ($interval->days <= $Days && ($interval->invert == 1 || $now_time->format("dd") == $event_start->format("dd"))) {
***REMOVED******REMOVED***$event_end = new DateTime($event["end"]);
***REMOVED******REMOVED***$interval = $event_end->diff($now_time);
***REMOVED******REMOVED***if ($interval->invert == 1) {
***REMOVED******REMOVED******REMOVED***array_push( $time_filtered_events_JSON, $event);
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***// echo json_encode($time_filtered_events_JSON, JSON_PRETTY_PRINT);

***REMOVED***$return_events_JSON = [];
***REMOVED***if ($Skip < count($time_filtered_events_JSON)) {
***REMOVED******REMOVED***for ($i = $Skip; $i < min(count($time_filtered_events_JSON), $Skip + $ShowEvent); $i++) {
***REMOVED******REMOVED***array_push( $return_events_JSON, $time_filtered_events_JSON[$i]);
***REMOVED***
***REMOVED***

***REMOVED***echo json_encode($return_events_JSON, JSON_PRETTY_PRINT);
***REMOVED***
***REMOVED***