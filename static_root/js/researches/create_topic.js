
const numr = document.getElementById('numr')

let second = "الموضوع 2",
    third = "الموضوع 3",
    fourht = "الموضوع 4",
    fifth = "الموضوع 5";
let nums = [0, 0, second, third, fourht, fifth];


function rr(trgt) {
    document.getElementById(`choose-sub-box-${trgt.id.slice(-1)}`).remove();
    if (Number(numr.value) > Number(trgt.id.slice(-1))) {
        for (let i = Number(trgt.id.slice(-1)) + 1; i <= Number(numr.value); i++) {
            let selectedBox = document.getElementById(`choose-sub-box-${i}`)
            selectedBox.id = `choose-sub-box-${i - 1}`;
            selectedBox.firstElementChild.id = `r-box-${i - 1}`
            selectedBox.lastElementChild.firstElementChild.id = `remover-${i - 1}`
            let title = nums[i - 1];
            selectedBox.firstElementChild.firstElementChild.innerText = title
            selectedBox.firstElementChild.lastElementChild.id = `subject-${i - 1}`
            selectedBox.firstElementChild.lastElementChild.name = `subject-${i - 1}`
            selectedBox.firstElementChild.lastElementChild.placeholder = title
            selectedBox.firstElementChild.firstElementChild.setAttribute('for', `subject-${i - 1}`)

        }
    }
    numr.value = `${Number(numr.value) - 1}`
    console.log(numr.value)
    let ourForm = document.getElementById("rinputs");
    let ourButtons = document.getElementById("buttons");
    if (numr.value == 1) {
        let ourButtons = document.getElementById("buttons");
        let newInner = `<div class="col-6"><button type="submit">إنهاء</button></div>
        <div class="col-6"><button type="button" id="another-subject" onclick="addr()">اضافة موضوع آخر</button></div>`;
        ourButtons.innerHTML = newInner;
    } else if (numr.value == 4) {
        let newInner = `<div class="col-6"><button type="submit">إنهاء</button></div>
            <div class="col-6"><button type="button" id="another-subject" onclick="addr()">اضافة موضوع آخر</button></div>`;
        ourButtons.innerHTML = newInner;
    }
}

document.getElementById("another-subject").onclick = addr
function addr() {
    console.log(numr)
    if (Number(numr.value) < 5) {
        let ourForm = document.getElementById("rinputs"),
            valuesBefore = [];
        for (let i = 0; i < Number(numr.value); i++) {
            
            let ourInput = ourForm.children[i].children[0].children[1];
            valuesBefore.push(ourInput.value)
        }
        numr.value = `${Number(numr.value) + 1}`
        
        let title = nums[Number(numr.value)];
        let ourButtons = document.getElementById("buttons");
        if (Number(numr.value) == 2) {
            let newInner = `<div class="col-6"><button type="submit">إنهاء</button></div>
            <div class="col-6"><button type="button" id="another-subject" onclick="addr()">اضافة موضوع آخر</button></div>`;
            ourButtons.innerHTML = newInner;
        } else if (Number(numr.value) == 5) {
            let newInner = `<div class="col-12"><button type="submit">إنهاء</button></div>`;
            ourButtons.innerHTML = newInner;
        }

        let ourAdd = `<div id="choose-sub-box-${numr.value}">
            <div class="col-12 item" id = "r-box-${numr.value}">
                <label for="subject-${numr.value}">${title}</label>
                <textarea name="subject-${numr.value}" id="subject-${numr.value}"  placeholder="${title}" oninvalid="(this.value) ? this.setCustomValidity('هذا البحث موجود من قبل') : this.setCustomValidity('يجب ملئ هذا الحقل')" oninput="input_clicked(this)" required></textarea>
            </div>
                <div class="col-12"><button type="button" id="remover-${numr.value}" class = "remover" onclick = "rr(this)" >حذف الموضوع</button></div>
            </div>
        </div>
        `;
        ourForm.innerHTML += ourAdd;

        for (let i = 0; i < Number(numr.value) - 1; i++) {
            let ourInput = ourForm.children[i].children[0].children[1];
            ourInput.value = valuesBefore[i]
        }
    }
}

