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

// Handle preflight requests
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit();
}

// API endpoint to upload user location
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the user's location from the request body
    $data = json_decode(file_get_contents('php://input'), true);

    // Input validation
    if (!isset($data['user_id']) || !is_numeric($data['user_id'])) {
        echo json_encode(array("error" => "Invalid user ID"));
        exit();
    }

    if (!isset($data['latitude']) || !is_numeric($data['latitude'])) {
        echo json_encode(array("error" => "Invalid latitude"));
        exit();
    }

    if (!isset($data['longitude']) || !is_numeric($data['longitude'])) {
        echo json_encode(array("error" => "Invalid longitude"));
        exit();
    }

    $user_id = $data['user_id'];
    $latitude = $data['latitude'];
    $longitude = $data['longitude'];

    // Prepare and bind the SQL statements
    $stmt = $conn->prepare("SELECT * FROM user_locations WHERE user_id = ?");
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $stmt = $conn->prepare("UPDATE user_locations SET latitude = ?, longitude = ? WHERE user_id = ?");
        $stmt->bind_param("ddi", $latitude, $longitude, $user_id);
    } else {
        $stmt = $conn->prepare("INSERT INTO user_locations (user_id, latitude, longitude) VALUES (?, ?, ?)");
        $stmt->bind_param("idd", $user_id, $latitude, $longitude);
    }

    if ($stmt->execute()) {
        echo json_encode(array("message" => "Location updated successfully"));
    } else {
        echo json_encode(array("error" => "Error: " . $stmt->error));
    }

    $stmt->close();
}

$conn->close();
?>