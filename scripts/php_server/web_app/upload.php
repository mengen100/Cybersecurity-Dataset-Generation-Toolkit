<?php
session_start();
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
    die("Unauthorized access");
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $target_dir = "uploads/";
    $target_file = $target_dir . basename($_FILES["file"]["name"]);
    
    if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) {
        echo "File uploaded successfully";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
</head>
<body>
    <h2>Upload File</h2>
    <form method="post" enctype="multipart/form-data">
        Select file to upload:
        <input type="file" name="file" id="file">
        <input type="submit" value="Upload File" name="submit">
    </form>
</body>
</html>