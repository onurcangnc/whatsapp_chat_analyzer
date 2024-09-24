$(document).ready(function(){
    // Disable the submit button initially
    $("#submitbtn").prop("disabled", true);  

    // Trigger file input on click of the browse button
    $('#btnup').click(function(){
        $('#fileup').click();  // Simulate click on hidden file input
    });

    // Validate the selected file
    $('#fileup').change(function(){
        var fileInput = $(this);  // The input element
        var filePath = fileInput.val();  // The file path
        var allowedExtensions = /(\.txt)$/i;  // Allowed file extensions (only .txt)

        // Check if file has been selected and if it is a .txt file
        if(filePath && allowedExtensions.exec(filePath)) {
            // Show valid icon, hide invalid icon, and enable submit button
            $(".imgupload").hide("slow");
            $(".imgupload.stop").hide("slow");
            $(".imgupload.ok").show("slow");
            
            var fileName = filePath.split('\\').pop();  // Extract file name
            $('#namefile').html(fileName).css({"color": "green", "font-weight": 700});
            $("#submitbtn").prop("disabled", false).show();  // Enable submit button
            $("#fakebtn").hide();  // Hide the fake button
        } else {
            // Invalid file, show error and disable submit button
            $(".imgupload").hide("slow");
            $(".imgupload.ok").hide("slow");
            $(".imgupload.stop").show("slow");

            $('#namefile').html("File is not a valid .txt file!").css({"color": "red", "font-weight": 700});
            $("#submitbtn").prop("disabled", true).hide();  // Disable submit button
            $("#fakebtn").show();  // Show the fake button
        }
    });
});
