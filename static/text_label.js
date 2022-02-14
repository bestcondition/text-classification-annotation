let glob_id = 0
let glob_filename = ''
let file_len = 0
let mark_map = new Map()
let mark_list = []
let key_code_mark_map = new Map()
//关键字突出颜色绑定
let keyword_color_map = new Map()
//绑定个鬼，直接遍历就行了
let keyword_color_list = new Array(0)


function last_txt() {
    document.getElementById('previous').click()
}

function next_txt() {
    document.getElementById('next').click()
}

function mod_id(id) {
    // 模id
    return (id + file_len) % file_len
}

function offset_id(offset) {
    backColor_white(glob_id)
    glob_id = mod_id(glob_id + offset)
    backColor_blue(glob_id)

    let text = document.getElementById("tr_" + glob_id)
    text.scrollIntoView({behavior: 'auto', block: 'nearest', inline: 'nearest'})
}


function last_label() {
    // add_label(glob_id) // 移动光标不应该保存，注意逻辑
    offset_id(-1)
}

function next_label() {
    // add_label(glob_id)// 移动光标不应该保存
    if (glob_id === file_len - 1) {
        next_txt()
    } else {
        offset_id(1)
    }
}

function backColor_blue(id) {
    let text = document.getElementById("tr_" + id)
    //不要对ide的黄色警告不管不顾，或许这正是优雅的开始
    // text.style.background = "lightblue"
    text.style.background = "#66ccff"
}

function backColor_white(id) {
    let text = document.getElementById("tr_" + id)
    text.style.background = "white"
}

function choice(id) {
    backColor_white(glob_id)
    glob_id = id
    backColor_blue(glob_id)
}

//设置按键map，显示按键
function introduce() {
    // //既定的按键，用着就用，用不着搁那，用多了就错
    // let key_list = new Array(0)
    //
    //
    // //添加到key_list
    // function add_num_key_1_to_9(code_prefix, show_prefix) {
    //     for (let i = 0; i < 9; i++) {
    //         let num = i + 1
    //         key_list.push(
    //             [code_prefix + num, show_prefix + num]
    //         )
    //     }
    // }
    //
    // add_num_key_1_to_9('Numpad', '小键盘')
    // add_num_key_1_to_9('Digit', '大键盘')

    for (let i = 0; i < mark_list.length; i++) {
        let mark = mark_list[i]
        // let key_code = key_list[i][0]
        // let show = key_list[i][1]
        //添加映射
        // key_code_mark_map.set(key_code, mark)

        //前端显示
        document.getElementById('num_' + i).innerText = '' + i
        document.getElementById('mark_' + i).innerText = mark

    }
}

async function add_label(mark) {
    let url = "/change/" + glob_id + "/" + mark
    console.log(url)
    //对fetch的response进行判断，错误至少要提示在前端
    let response = await fetch(url)
    if (response.ok) {
        return true
    } else {
        alert(await response.text())
        return false
    }
}

//将从后端拿到的keyword转换成list
function convert_keyword_color_map() {
    for (let keyword in keyword_color_map) {//这里是对象，用in遍历属性
        if (keyword_color_map.hasOwnProperty(keyword)) {//fuck ide
            let color = keyword_color_map[keyword]
            let reg = new RegExp(keyword)
            keyword_color_list.push([reg, color])
        }
    }
}

function b_u_i_tech() {
    convert_keyword_color_map()

    for (let i = 0; i < file_len; i++) {
        let dom = document.getElementById('text_' + i)
        for (let reg_color of keyword_color_list) {
            let reg = reg_color[0]
            let color = reg_color[1]
            dom_keyword_color(dom, reg, color)
        }
    }
}

function dom_keyword_color(dom, keyword, color) {
    dom.innerHTML = dom.innerHTML.replace(keyword, '<b style="color: ' + color + '">$&</b>')
}

KEY_STATUS = {
    NO_RETURN: {},
    NO_VALUE: {},
}

function TwoDigitsInput() {
    //第一位
    this.first = KEY_STATUS.NO_VALUE
    //第二位
    this.second = KEY_STATUS.NO_VALUE
    //发送监听事件
    this.send = function (e) {
        let match = /(Digit|Numpad)(\d)/.exec(e.code)
        //匹配到
        if (match) {
            let mode = match[1]
            let num = parseInt(match[2])
            if (this.first !== KEY_STATUS.NO_VALUE) {//第一个有值
                this.second = num
            } else {//第一个没值
                if (mode === 'Numpad') {//按的小键盘
                    this.first = 0
                    this.second = num
                } else { // 按的大键盘
                    this.first = num
                }
            }
            //看看能不能返回
            return this.ret()
        }
    }
    this.ret = function () {
        if (this.first !== KEY_STATUS.NO_VALUE && this.second !== KEY_STATUS.NO_VALUE) {
            let value = this.first * 10 + this.second
            this.reset()
            return value
        } else {
            return KEY_STATUS.NO_RETURN
        }
    }
    //重置两个位
    this.reset = function () {
        this.first = KEY_STATUS.NO_VALUE
        this.second = KEY_STATUS.NO_VALUE
    }
}

let num_input = new TwoDigitsInput()

function add_listener() {
    document.addEventListener('keydown', async function (e) {
        if (e.code === 'ArrowLeft')
            last_txt()
        else if (e.code === 'ArrowRight')
            next_txt()
        else if (e.code === 'ArrowUp')
            last_label()
        else if (e.code === 'ArrowDown')
            next_label()
        else {
            // let match = /(Digit|Numpad)(\d)/.exec(e.code)
            // if (match) {
            //     let mode = match[1]
            //     let num = match[2]
            //     let mark = mode === "Digit" ? num : '1' + num
            let num = num_input.send(e)
            if (num !== KEY_STATUS.NO_RETURN) {
                if (num < mark_list.length) {
                    let mark = mark_list[num]
                    let flag = await add_label(mark)
                    if (flag) {//判断是否添加成功
                        document.getElementById("label_" + glob_id).innerText = mark//成功了才更数字
                        next_label()//成功了才下一个
                        // }
                    }
                }
            }

        }
    })
}
