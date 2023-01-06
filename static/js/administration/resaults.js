const selects = document.getElementById('selects');

function fill_table(iterable=[]){
    const studentsTable = document.getElementById('result-table');
    studentsTable.innerHTML="";
    let span=0;
    for(let student of iterable){
        span = student.researches.length
        if(span != 0){
            studentsTable.innerHTML+=`
                <tr>
                    <td rowspan="${span}" scope="row">${student.name}</td>
                    <td>${student.researches[0].subject}</td>
                    <td>${student.researches[0].name}</td>

                    <td>${student.researches[0].intro}</td>
                    <td>${student.researches[0].axes}</td>
                    <td>${student.researches[0].content}</td>
                    <td>${student.researches[0].conclusions}</td>
                    <td>${student.researches[0].references}</td>
                    <td>${student.researches[0].total}</td>

                    <td><span class="${(student.researches[0].passed == "مستوفي") ? 'passed' : "not-passed"}">${student.researches[0].passed}</span></td>
                </tr>
            `
            if(span > 1){
                for(let research of student.researches.slice(1))
                    studentsTable.innerHTML += `
                    <tr>
                        <td>${research.subject}</td>
                        <td>${research.name}</td>

                        <td>${research.intro}</td>
                        <td>${research.axes}</td>
                        <td>${research.content}</td>
                        <td>${research.conclusions}</td>
                        <td>${research.references}</td>
                        <td>${research.total}</td>
    
                        <td><span class="${(research.passed == "مستوفي") ? 'passed' : "not-passed"}">${research.passed}</span></td>
                    </tr>
                `
            }
        }   
    }
}

// ADMIN
if(user.admin){
    selects.innerHTML = `
        <select id="faculties" oninput="select_selected(this)">
            <option value="">جميع الكليات</option>
        </select>
        <select id="teams" oninput="select_selected(this)">
            <option value="">جميع الفرق</option>
        </select>
        <select id="subjects" oninput="select_selected(this)">
            <option value="">جميع المقررات</option>
        </select>
    `
    const facultySelect = document.getElementById('faculties');
    for(let faculty of jfaculties){

        facultySelect.innerHTML += `
            <option value="${faculty.name}">${faculty.name}</option>
        `
    }
    fill_table(jstudents)

// STAFF
}else if(user.staff){

    selects.innerHTML = `
        <select id="teams" oninput="select_selected(this)">
            <option value="">جميع الفرق</option>
        </select>
        <select id="subjects" oninput="select_selected(this)">
            <option value="">جميع المقررات</option>
        </select>
    `
    const teamSelect = document.getElementById('teams');
    for (let team of jfaculties.find(f => f.name == user.faculty).teams) {
        teamSelect.innerHTML += `
            <option value="${team.name}">${team.name}</option>
        `
    }
    fill_table(jstudents.filter(s => s.faculty == user.faculty))


// CONTROL_HEAD
}else{
    selects.innerHTML = `
        <select id="subjects" oninput="select_selected(this)">
            <option value="">جميع المقررات</option>
        </select>
    `
    const subjectSelect = document.getElementById('subjects');
    for (let subject of jfaculties.find(f => f.name == user.faculty).teams.find(t => t.name == user.team).subjects) {
        subjectSelect.innerHTML += `
            <option value="${subject.name}">${subject.name}</option>
        `
    }
    fill_table(jstudents.filter(s => s.faculty == user.faculty).filter(s => s.team == user.team))

}

function select_selected(trgt){
    const selectedValue = trgt.value,
          studentsTable = document.getElementById('result-table');
    // FACULTIES
    if(trgt.id=="faculties"){
        const teamSelect = document.getElementById('teams'),
            subjectSelect = document.getElementById('subjects');

        teamSelect.innerHTML = '<option value="">جميع الفرق</option>';
        subjectSelect.innerHTML = '<option value="">جميع المقررات</option>'

        if(selectedValue){
            
            // selects

            for (let team of jfaculties.find(f => f.name == selectedValue).teams) {
                teamSelect.innerHTML += `
                    <option value="${team.name}">${team.name}</option>
                `
            }
            
            // data
            fill_table(jstudents.filter(s => s.faculty == selectedValue))
        } else {
            // data
            fill_table(jstudents)

        }



    // TEAMS
    } else if (trgt.id == "teams"){
        const facultySelect = document.getElementById('faculties'),
            subjectSelect = document.getElementById('subjects');

        subjectSelect.innerHTML = '<option value="">جميع المقررات</option>'

        if (selectedValue) {
            
            // selects

            for (let subject of jfaculties.find(f => (facultySelect == null) ? f.name == user.faculty : f.name == facultySelect.value).teams.find(t => t.name == selectedValue).subjects) {
                subjectSelect.innerHTML += `
                    <option value="${subject.name}">${subject.name}</option>
                `
            }

            // data
            fill_table(jstudents.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value).filter(s => s.team == selectedValue))

        } else {
            // data
            fill_table(jstudents.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value))

        }



    // SUBJECTS
    }else{
        const teamSelect = document.getElementById('teams'),
            facultySelect = document.getElementById('faculties');

            if (selectedValue) {
            
            // data
            studentsTable.innerHTML = "";
            let span = 0;
            for (let student of jstudents.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value).filter(s => (teamSelect == null) ? s.team == user.team : s.team == teamSelect.value)) {
                nr = student.researches.find(r => r.subject == selectedValue)
                span = nr.length
                if (span != 0) {
                    studentsTable.innerHTML += `
                    <tr>
                        <td rowspan="${span}" scope="row">${student.name}</td>
                        <td>${nr.subject}</td>
                        <td>${nr.name}</td>

                        <td>${nr.intro}</td>
                        <td>${nr.axes}</td>
                        <td>${nr.content}</td>
                        <td>${nr.conclusions}</td>
                        <td>${nr.references}</td>
                        <td>${nr.total}</td>

                        <td><span class="${(nr.passed == "مستوفي") ? 'passed' : "not-passed"}">${nr.passed}</span></td>
                    </tr>
                `
                }
            }
        } else {
            //data
            fill_table(jstudents.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value).filter(s => (teamSelect == null) ? s.team == user.team : s.team == teamSelect.value))
        }
    }
}

function export_excel(){
    const studentsTable = document.getElementById('result-table').parentElement;
    var wb = XLSX.utils.book_new();
    wb.Props = {
        Title: "نتائج الطلبة",
        Subject: "النتائج",
        Author: "منصة المواضيع البحثية",
        CreatedDate: new Date()
    };
    wb.SheetNames.push("النتائج");
    //here
    var wb = XLSX.utils.table_to_book(studentsTable, { sheet: "Sheet JS" });
    var ws = XLSX.utils.aoa_to_sheet([['he']]);
    //
    wb.Sheets["النتائج"] = ws;
    var wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'base64' });
    XLSX.writeFile(wb, 'resaults.xlsx');

}
