// Variable de objetos
let d = document,
  c = console.log;
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener("DOMContentLoaded", function (e) {
  // Declaracion de variables
  let $nquota = d.getElementById("nquota");
  let $status = d.getElementById("status");
  let $date_discount = d.getElementById("date_discount");
  let $balance = d.getElementById("balance_quota");
  let $btnadd = d.getElementById("btnadd");
  let $detailBody = d.getElementById("detalle");
  let $btnGrabar = d.getElementById("btnGrabar");
  let $form = d.getElementById("form-container");
  let detailCredit = [];
  if (detail.length > 1) {
    detailCredit = detail.map((item) => {
      const { id: id, dat: date, quot: quota, nh, bal: balance } = item;
      return { id, date, quota, nh, balance };
    });
    present();
  }

  // Declaracion de metodos
  function present() {
    c("estoy en present()");
    let detalle = document.getElementById("detalle");
    detalle.innerHTML = "";
    detailCredit.forEach((credit) => {
      detalle.innerHTML += `<tr>
            <td>${credit.id}</td>
            <td>${credit.date}</td>
            <td>${credit.quota}</td>
            <td>${credit.nh}</td>
            <td>${credit.balance}</td>
            <td><a href="#" class="delete" data-id="${credit.id}">Eliminar</a></td>
        </tr>`;
    });
  }

  $btnadd.addEventListener("click", (e) => {
    e.preventDefault();
    let id = $nquota.value;
    let date = $date_discount.value;
    let quota = $nquota.value;
    let nh = $nquota.value;
    let balance = $balance.value;
    detailCredit.push({ id, date, quota, nh, balance });
    present();
  });

  $form.addEventListener("submit", (e) => {
    e.preventDefault();
    let $csrfmiddlewaretoken = d.getElementsByName("csrfmiddlewaretoken")[0];
    let $employee = d.getElementById("id_employee");
    let $type = d.getElementById("id_type");
    let $datei = d.getElementById("id_date_initial");
    let $datec = d.getElementById("id_date_credit");
    let $amount = d.getElementById("id_amount");
    let $status = d.getElementById("id_status");
    let $detail_credit = d.getElementById("id_detail_credit");
    $detail_credit.value = JSON.stringify(detailCredit);
    let data = {
      csrfmiddlewaretoken: $csrfmiddlewaretoken.value,
      employee: $employee.value,
      type: $type.value,
      datei: $datei.value,
      datec: $datec.value,
      amount: $amount.value,
      detail: $detail.value,
      status: $status.value,
      detail_credit: $detail_credit.value,
    };
    c(data);
    fetch("", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data) => {
        c(data);
        if (data.ok) {
          location.href = data.url;
        } else {
          alert(data.message);
        }
      });
  });
  // ---------- envia los datos del sobretiempo al backend por ajax para grabarlo ----------
  $form.addEventListener("submit", async (e) => {
    e.preventDefault();
    // if (parseFloat(d.getElementById("id_total").value) > 0.0) {
    const formData = new FormData($form);
    formData.append("detail", JSON.stringify(detailCredit));
    const employee = await fetchPost(location.pathname, formData);
    console.log(employee);
    if (!employee.ok) return c(employee.data);
    window.location = backUrl;
    // } else {
    //   alert("!!!Ingrese horas de sobretiempo para grabar!!!");
    // }
  });
  // -------- registra las horas del sobretiempo en el arreglo detailOvertime[] ---------

  //---- por delegacion de eventos seleccionada la fila de las horas del sobretiempo ----------
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener("click", (e) => {
    const fil = e.target.closest("button[rel=rel-delete]");
    if (fil) deleteHours(parseInt(fil.dataset.id));
  });
});
