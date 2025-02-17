
var address = undefined     //A Global variable will store location
$('a[class="search-btn"]').on('click', (e)=>{
    // alert('Wait a minute.')
    e.preventDefault()
    let value = $('#unique').val()
    $('#unique').val('')
    address = value
    clearData()
    start()
})

$(document).ready(()=>{
    /**Late will be implement hourly update weather 
     * casting.
    */
    console.log('Feeling Alive.')
    if(address != undefined){
        let date = new Date();
        console.log(`Address was ${address}.`)
        $.get(
            `/api/hour/${address}/${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}?hour=${date.getHours()}`,
        ).done((data)=>{
            console.log('Here was data ', data)
            placeData(data)        
        })
        createTable()       //table was created
    }
})

function start(){
    let date = new Date();
    $.get(
        `/api/hour/${address}/${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}?hour=${date.getHours()}`,
    ).done((data)=>{
        console.log('Here was data ', data)    
        placeData(data)    
    })
    createTable()       //table was created
}
function changeBgColor(timer) {
    let colors = [
 '#348AC7', '#5cbdbb', 'aqua','aquamarine', 'orangered', 'orchid', 'magenta'
                ]
    let index = 0

    setTimeout(()=>{
        if(index == colors.length){
            index = 0
        }else{
            index++
        }
        $('body').css('background-color', colors[index])
    }, timer)
}

function placeData(data) {
    /**This function will place data on template 
     * base one where it require  */    
    let temp = (5/9 * (data.temp - 32)).toString().split('.')[0]    //Ferhenite to Celcius convertion
    //only take front part of period on that 
    $('.title').text(data.location)
    $('.short-loc').text(address)
    console.log('Here was data from placeData ', Math.round(data.snow))
    increaseTemp(temp, 50)  //set temprature
    increaseNum($('.rain'), Math.round(data['snow']), 'MM')     //adjust rain
    increaseNum($('.wind'), Math.round(data['windspeed']), 'MPH')     //adjust wind
    increaseNum($('.humidity'), Math.round(data.humidity))     //adjust humidity
    increaseNum($('.uv'), Math.round(data.uvindex))     //adjust uv
    increaseNum($('.pressure'), Math.round(data.pressure), undefined, 1)     //adjust air pressure
}

function clearData(){
    /**This function will clear somedata and set its
     * default value.
    */
    $('.temp').html('0&deg;')
    $('.short-loc').text(' ')
    $('.rain').text('0 MM')
    $('.wind').text('0 MPH')
    let children = $('#table-con').children()
    for(let i =0 ; i < children.length; i++){
        $(children[i]).remove()
    }
    $('.humidity').text('0')
    $('.uv').text('0')
    $('.pressure').text('0')
}   

function increaseTemp(limit, timer, unit = '\u00B0', defaultVal = 0){
    /**This will increase number base on a timer */
    let temp = $('.temp')
    let interId = setInterval(
        ()=>{
            temp.text(defaultVal+unit)
            if(defaultVal == limit){
                clearInterval(interId)
            }
            defaultVal++
        }, timer
    )
}

function increaseNum(target, limit, unit = undefined, timer = 50, defaultVal = 0){
    /**This will increase number base on a timer */
    let interId = setInterval(
        ()=>{
            if(unit != undefined){
                $(target).text(defaultVal+' '+unit)
            }else{
                $(target).text(defaultVal)
            }
            if(defaultVal == limit){
                clearInterval(interId)
            }
            defaultVal++
        }, timer
    )
}

function createTable() {
    let date = new Date()
    let hour = date.getHours() + 1
    let remainHour = 23 - hour
    let thCon = $('<tr>')
    let tdCon = $('<tr>')
    for(let i = 0; i <= remainHour; i++){
        thCon.append($(`<th>${hour}:00</th>`))
        $.get(`/api/hour/${address}/${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}?hour=${date.getHours()+i}`)
        .done((data)=>{
            tdCon.append(`<td>${ferheniteToCelcius(data['temp'])}\u00B0 C</td>`)
        })
        hour++
    }
    $('#table-con').append(thCon)
    $('#table-con').append(tdCon)
}

function ferheniteToCelcius(value) {
    /**This function will return ferhenite value 
     * to celcius value
     */
    // console.log('Here was another value ', value)
    value = parseInt(value)
    return (5/9 * (value -32)).toFixed()
}