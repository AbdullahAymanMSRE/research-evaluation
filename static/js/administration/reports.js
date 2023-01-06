const selects = document.getElementById('selects');

// ADMIN
if (user.admin) {
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
    for (let faculty of jfaculties) {

        facultySelect.innerHTML += `
            <option value="${faculty.name}">${faculty.name}</option>
        `
    }
    const subjectsTable = document.getElementById('result-table');
    let span = 0;
    for (let subject of jsubjects) {
        span = subject.researches.length
        if (span != 0) {
            subjectsTable.innerHTML += `
                <tr>
                    <td rowspan="${span}" scope="row">${subject.name}</td>
                    <td>${subject.researches[0].name}</td>
                    <td>${subject.researches[0].asr}</td>
                    <td>${subject.researches[0].csr}</td>
                </tr>
            `
            if (span > 1) {
                for (let research of subject.researches.slice(1))
                    subjectsTable.innerHTML += `
                    <tr>
                        <td>${research.name}</td>
                        <td>${research.asr}</td>
                        <td>${research.csr}</td>
                    </tr>
                `
            }
        }
    }

// STAFF
} else if (user.staff) {

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

    const subjectsTable = document.getElementById('result-table');
    let span = 0;
    for (let subject of jsubjects.filter(s => s.faculty == user.faculty)) {
        span = subject.researches.length
        if (span != 0) {
            subjectsTable.innerHTML += `
                    <tr>
                        <td rowspan="${span}" scope="row">${subject.name}</td>
                        <td>${subject.researches[0].name}</td>
                        <td>${subject.researches[0].asr}</td>
                        <td>${subject.researches[0].csr}</td>
                    </tr>
                `
            if (span > 1) {
                for (let research of subject.researches.slice(1))
                    subjectsTable.innerHTML += `
                        <tr>
                            <td>${research.name}</td>
                            <td>${research.asr}</td>
                            <td>${research.csr}</td>
                        </tr>
                    `
            }
        }
    }


// CONTROL_HEAD
} else {

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

    const subjectsTable = document.getElementById('result-table');
    let span = 0;
    for (let subject of jsubjects.filter(s => s.faculty == user.faculty).filter(s => s.team == user.team)) {
        span = subject.researches.length
        if (span != 0) {
            subjectsTable.innerHTML += `
                    <tr>
                        <td rowspan="${span}" scope="row">${subject.name}</td>
                        <td>${subject.researches[0].name}</td>
                        <td>${subject.researches[0].asr}</td>
                        <td>${subject.researches[0].csr}</td>
                    </tr>
                `
            if (span > 1) {
                for (let research of subject.researches.slice(1))
                    subjectsTable.innerHTML += `
                        <tr>
                            <td>${research.name}</td>
                            <td>${research.asr}</td>
                            <td>${research.csr}</td>
                        </tr>
                    `
            }
        }
    }

}

function select_selected(trgt) {
    const selectedValue = trgt.value;
    // FACULTIES
    if (trgt.id == "faculties") {
        const teamSelect = document.getElementById('teams'),
            subjectSelect = document.getElementById('subjects'),
            subjectsTable = document.getElementById('result-table');

        teamSelect.innerHTML = '<option value="">جميع الفرق</option>';
        subjectSelect.innerHTML = '<option value="">جميع المقررات</option>'

        if (selectedValue) {
            // selects

            for (let team of jfaculties.find(f => f.name == selectedValue).teams) {
                teamSelect.innerHTML += `
                    <option value="${team.name}">${team.name}</option>
                `
            }

            // data
            subjectsTable.innerHTML = "";
            let span = 0;
            for (let subject of jsubjects.filter(s => s.faculty == selectedValue)) {
                span = subject.researches.length
                if (span != 0) {
                    subjectsTable.innerHTML += `
                    <tr>
                        <td rowspan="${span}" scope="row">${subject.name}</td>
                        <td>${subject.researches[0].name}</td>
                        <td>${subject.researches[0].asr}</td>
                        <td>${subject.researches[0].csr}</td>
                    </tr>
                `
                    if (span > 1) {
                        for (let research of subject.researches.slice(1))
                            subjectsTable.innerHTML += `
                        <tr>
                            <td>${research.name}</td>
                            <td>${research.asr}</td>
                            <td>${research.csr}</td>
                        </tr>
                    `
                    }
                }
            }
        } else {
            // data
            subjectsTable.innerHTML = "";
            let span = 0;
            for (let subject of jsubjects) {
                span = subject.researches.length
                if (span != 0) {
                    subjectsTable.innerHTML += `
                        <tr>
                            <td rowspan="${span}" scope="row">${subject.name}</td>
                            <td>${subject.researches[0].name}</td>
                            <td>${subject.researches[0].asr}</td>
                            <td>${subject.researches[0].csr}</td>
                        </tr>
                    `
                    if (span > 1) {
                        for (let research of subject.researches.slice(1))
                            subjectsTable.innerHTML += `
                            <tr>
                                <td>${research.name}</td>
                                <td>${research.asr}</td>
                                <td>${research.csr}</td>
                            </tr>
                        `
                    }
                }
            }

        }



    // TEAMS
    } else if (trgt.id == "teams") {
        const facultySelect = document.getElementById('faculties'),
            subjectSelect = document.getElementById('subjects'),
            subjectsTable = document.getElementById('result-table');

        subjectSelect.innerHTML = '<option value="">جميع المقررات</option>'

        if (selectedValue) {
            // selects

            for (let subject of jfaculties.find(f => (facultySelect == null) ? f.name == user.faculty : f.name == facultySelect.value).teams.find(t => t.name == selectedValue).subjects) {
                subjectSelect.innerHTML += `
                    <option value="${subject.name}">${subject.name}</option>
                `
            }

            // data
            subjectsTable.innerHTML = "";
            let span = 0;
            for (let subject of jsubjects.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value).filter(s => s.team == selectedValue)) {
                span = subject.researches.length
                if (span != 0) {
                    subjectsTable.innerHTML += `
                        <tr>
                            <td rowspan="${span}" scope="row">${subject.name}</td>
                            <td>${subject.researches[0].name}</td>
                            <td>${subject.researches[0].asr}</td>
                            <td>${subject.researches[0].csr}</td>
                        </tr>
                    `
                    if (span > 1) {
                        for (let research of subject.researches.slice(1))
                            subjectsTable.innerHTML += `
                        <tr>
                            <td>${research.name}</td>
                            <td>${research.asr}</td>
                            <td>${research.csr}</td>
                        </tr>
                    `
                    }
                }
            }
        } else {
            // data
            subjectsTable.innerHTML = "";
            let span = 0;
            for (let subject of jsubjects.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value)) {
                span = subject.researches.length
                if (span != 0) {
                    subjectsTable.innerHTML += `
                        <tr>
                            <td rowspan="${span}" scope="row">${subject.name}</td>
                            <td>${subject.researches[0].name}</td>
                            <td>${subject.researches[0].asr}</td>
                            <td>${subject.researches[0].csr}</td>
                        </tr>
                    `
                    if (span > 1) {
                        for (let research of subject.researches.slice(1))
                            subjectsTable.innerHTML += `
                            <tr>
                                <td>${research.name}</td>
                                <td>${research.asr}</td>
                                <td>${research.csr}</td>
                            </tr>
                        `
                    }
                }
            }

        }



    // SUBJECTS
    } else {
        const teamSelect = document.getElementById('teams'),
            facultySelect = document.getElementById('faculties'),
            subjectsTable = document.getElementById('result-table');

        if (selectedValue) {
            // data
            subjectsTable.innerHTML = "";
            let span = 0;
            subject = jsubjects.find(s => s.name == selectedValue)
            span = subject.researches.length
            if (span != 0) {
                subjectsTable.innerHTML += `
                    <tr>
                        <td rowspan="${span}" scope="row">${subject.name}</td>
                        <td>${subject.researches[0].name}</td>
                        <td>${subject.researches[0].asr}</td>
                        <td>${subject.researches[0].csr}</td>
                    </tr>
                `
                if (span > 1) {
                    for (let research of subject.researches.slice(1))
                        subjectsTable.innerHTML += `
                            <tr>
                                <td>${research.name}</td>
                                <td>${research.asr}</td>
                                <td>${research.csr}</td>
                            </tr>
                        `
                }
            }
        } else {
            //data
            subjectsTable.innerHTML = "";
            let span = 0;
            for (let subject of jsubjects.filter(s => (facultySelect == null) ? s.faculty == user.faculty : s.faculty == facultySelect.value).filter(s => (teamSelect == null) ? s.team == user.team : s.team == teamSelect.value)) {
                span = subject.researches.length
                if (span != 0) {
                    subjectsTable.innerHTML += `
                    <tr>
                        <td rowspan="${span}" scope="row">${subject.name}</td>
                        <td>${subject.researches[0].name}</td>
                        <td>${subject.researches[0].asr}</td>
                        <td>${subject.researches[0].csr}</td>
                    </tr>
                `
                    if (span > 1) {
                        for (let research of subject.researches.slice(1))
                            subjectsTable.innerHTML += `
                        <tr>
                            <td>${research.name}</td>
                            <td>${research.asr}</td>
                            <td>${research.csr}</td>
                        </tr>
                    `
                    }
                }
            }
        }
    }
}

function export_excel() {
    const subjectsTable = document.getElementById('result-table').parentElement;
    var wb = XLSX.utils.book_new();
    wb.Props = {
        Title: "التقارير",
        Subject: "تقارير رفع وتصحيح المقررات",
        Author: "منصة المواضيع البحثية",
        CreatedDate: new Date()
    };
    wb.SheetNames.push("التقارير");
    //here
    var wb = XLSX.utils.table_to_book(subjectsTable, { sheet: "Sheet JS" });
    var ws = XLSX.utils.aoa_to_sheet([['he']]);
    //
    wb.Sheets["التقارير"] = ws;
    var wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'base64' });
    XLSX.writeFile(wb, 'resaults.xlsx');

}