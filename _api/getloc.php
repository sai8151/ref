<?php
// Database configuration
$servername = "localhost";
$username = "1234";
$password = "1234";
$database = "1234";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// API endpoint to retrieve user location
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $user_id = $_GET['user_id'];

    $stmt = $conn->prepare("SELECT latitude, longitude FROM user_locations WHERE user_id = ?");
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        echo json_encode(array("latitude" => $row['latitude'], "longitude" => $row['longitude']));
    } else {
        echo json_encode(array("message" => "Location not found"));
    }

    $stmt->close();
}

$conn->close();
?>