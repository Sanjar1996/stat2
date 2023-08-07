const convertToObj = arr => {
   return arr.map(elem => {
        if(elem){
            let obj = {id: elem.pk, name: elem.fields['name'] }
            return obj
        } else return false
    })
}
// Department
const convertToJson = arr => {
   return  arr.map(elem => {
        if(elem){
            let obj = {id: elem.pk, name: elem.fields['name'], region: elem.fields['region']}
            return obj
        }
    });
}

const getCsrfToken = arr =>  {
    let csrfToken = '';
        for (let i = 0; i < arr.length; ++i) {
            if (arr[i].name === 'csrfmiddlewaretoken') {
                csrfToken = arr[i].value;
                break;
            }
        }
        return csrfToken;
};
function numberWithSpaces(x) {
    let parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return parts.join(".");
}

function successMessage(msg){
    return Swal.fire({
          type: 'success',
          title: msg,
          showConfirmButton: false,
          timer: 1500
        })
}
function errorMessage(msg, t=1500){
    return Swal.fire({
          type: 'error',
          title: msg,
          showConfirmButton: false,
          timer: t
    })
}

function warningMessage(msg){
    return Swal.fire({
          type: 'warning',
          title: msg,
          showConfirmButton: false,
          timer: 1500
    })
}