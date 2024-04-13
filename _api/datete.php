<?php
// delete.php

// Check if authentication is valid
$authKey = $_GET['authKey']; // Assuming authKey is passed via GET parameter

// Validate authKey (you should have your own validation logic here)
if ($authKey !== 'iith') {
    http_response_code(401); // Unauthorized
    echo "Unauthorized access!";
    //exit;
}

$fileID = $_GET['fileID']; // Assuming fileID is passed via GET parameter
$conn = new mysqli('localhost', '1234', '1234', '1234');

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT file_name FROM uploads WHERE id = $fileID";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $file = 'uploads/' . $row['file_name'];

    // Check if the file exists
    if (file_exists($file)) {
        // Delete file from the server
        if (unlink($file)) {
            // Delete file metadata from the database
            $sql = "DELETE FROM uploads WHERE id = $fileID";
            if ($conn->query($sql) === TRUE) {
                echo "File deleted successfully.";
            } else {
                echo "Error deleting file: " . $conn->error;
            }
        } else {
            echo "Unable to delete the file.";
        }
    } else {
        echo "File not found.";
    }
} else {
    echo "File not found.";
}
$conn->close();
?>
