
const myForm = document.getElementById("myForm")
const allFilePath = document.getElementById("formFileAll")
const dailyFilePath = document.getElementById("formFileDaily")


allFilePath.addEventListener("change" , (e) =>{
    console.log(allFilePath.files[0].name)
    $("#AllPreview").attr("data", "/src/temp/" + allFilePath.files[0].name ) 
})

dailyFilePath.addEventListener("change" , (e) =>{
    console.log(e)
})
