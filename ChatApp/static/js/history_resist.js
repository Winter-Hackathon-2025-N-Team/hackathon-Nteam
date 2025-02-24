//csvを取り込み終わったら、処理開始
document.addEventListener("DOMContentLoaded", async function () {
    try {
        //幼稚園データの処理
        const responseKindergarten = await fetch("/static/data/kindergarten_master.json");
        const schoolDataKindergarten = await responseKindergarten.json();

        //小学校データの処理
        const responseElementary = await fetch("/static/data/elementary_master.json");
        const schoolDataElementary = await responseElementary.json();
        
        //データを1つのオブジェクトにまとめる処理
        const schoolData = {
            kindergarten_nensyo: schoolDataKindergarten,
            kindergarten_nenchu: schoolDataKindergarten,
            kindergarten_nencho: schoolDataKindergarten,
            elementary1: schoolDataElementary,
            elementary2: schoolDataElementary,
            elementary3: schoolDataElementary,
            elementary4: schoolDataElementary,
            elementary5: schoolDataElementary,
            elementary6: schoolDataElementary,
        }

        // すべての県セレクトボックスを取得
        document.querySelectorAll(".prefectures").forEach(prefSelect => {
            const category = prefSelect.getAttribute("data-id");
            const prefectures = [...new Set(schoolData[category].map(s => s.prefectures))];

            prefectures.forEach(pref => {
                let option = document.createElement("option");
                option.value = pref;
                option.textContent = pref;
                prefSelect.appendChild(option);
            });

            // 県が選択されたら市を更新
            prefSelect.addEventListener("change", function () {
                const citySelect = document.querySelector(`.municipalities[data-id="${category}"]`);
                const schoolSelect = document.querySelector(`.school_name[data-id="${category}"]`);

                citySelect.innerHTML = '<option value="">選択してください</option>';
                schoolSelect.innerHTML = '<option value="">選択してください</option>';

                if (this.value) {
                    citySelect.disabled = false;  // 都道府県が選択されたら市区町村を有効化
                } else {
                    citySelect.disabled = true;
                    schoolSelect.disabled = true;
                }

                const selectedPref = this.value;
                const cities = [...new Set(schoolData[category].filter(s => s.prefectures === selectedPref).map(s => s.municipalities))];

                cities.forEach(city => {
                    let option = document.createElement("option");
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            });
        });

        // すべての市セレクトボックスにイベント追加
        document.querySelectorAll(".municipalities").forEach(citySelect => {
            citySelect.addEventListener("change", function () {
                const category = this.getAttribute("data-id");
                const schoolSelect = document.querySelector(`.school_name[data-id="${category}"]`);
                schoolSelect.innerHTML = '<option value="">選択してください</option>';

                if (this.value) {
                    schoolSelect.disabled = false;  // 市区町村が選択されたら学校を有効化
                } else {
                    schoolSelect.disabled = true;
                }

                const selectedPref = document.querySelector(`.prefectures[data-id="${category}"]`).value;
                const selectedCity = this.value;
                const schools = schoolData[category]
                    .filter(s => s.prefectures === selectedPref && s.municipalities === selectedCity)
                    .map(s => s.school_name);

                schools.forEach(school => {
                    let option = document.createElement("option");
                    option.value = school;
                    option.textContent = school;
                    schoolSelect.appendChild(option);
                });
            });
        });
    } catch (error) {
        console.error("エラー:", error);
    }
});