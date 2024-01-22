// Variable de objetos
let d = document,
  c = console.log;
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener("DOMContentLoaded", function(e) {
  // Declaracion de variables
  let $nquota = d.getElementById("nquota");
  let $quotas = d.getElementById("id_nume_quota");
  let $status = d.getElementById("status");
  let $date_discount = d.getElementById("date_discount");
  let $balance = d.getElementById("balance_quota");
  let $btnadd = d.getElementById("btnadd");
  let $detailBody = d.getElementById("detalle");
  let $form = d.getElementById("form-container");
  let detailCredit = [];
  if (detail.length > 0) {
    detailCredit = detail.map((item) => {
      const {
        det_id: id,
        date: date,
        quote: quote,
        // status: status,
        bal: balance,
      } = item;
      return { id, quote, date, balance };
    });
    present();
  }

  function present() {
    let detalle = document.getElementById("detalle");
    detalle.innerHTML = "";
    detailCredit.forEach((detail) => {
      // let state = detail.status ? "procesado" : "pendiente";
            // <td>${state}</td>
      detalle.innerHTML += `<tr>
            <td>${detail.quote}</td>
            <td>${detail.balance}</td>
            <td>${detail.date}</td>
            <td>
            <td class="text-center ">
            <button rel="rel-delete" data-id="${detail.quote}" class="text-danger" data-bs-toggle="tooltip" data-bs-title="Eliminar registro"><i class="bi bi-x-circle-fill"></i></button>
        </td>
            </tr>`;
    });
  }

  $btnadd.addEventListener("click", (e) => {
    let existe = detailCredit.some((detail) => detail.quote == $nquota.value);
    if (!existe) {
      if ($nquota.value <= $quotas.value) {
        e.preventDefault();
        let date = $date_discount.value;
        let quote = $nquota.value;
        // let status = $status.value == "on" ? true : false;
        // console.log(status)
        let balance = $balance.value;
        detailCredit.push({ date, quote, status, balance });
        present();
      } else {
        let detalle = document.getElementById("detalle");
        detalle.innerHTML += `<p id="error_cuota">no puede agregar más cuotas de las establecidas</p>`;
        let error = document.getElementById("error_cuota");
        error.style.color = "red";
      }
    } else {
      let detalle = document.getElementById("detalle");
      detalle.innerHTML += `<p id="error_cuota">ya existe una cuota con ese numero</p></p>`;
      let error = document.getElementById("error_cuota");
      error.style.color = "red";
    }
  });

  $form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData($form);
    formData.append("detail", JSON.stringify(detailCredit));
    const request = await fetchPost(location.pathname, formData);
    if (!request.ok) return c(request);
    window.location = backUrl;
  });

  const deleteHours = (id) => {
    detailCredit = detailCredit.filter((item) => item.quote !== id);
    present();
  };
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener("click", (e) => {
    const fil = e.target.closest("button[rel=rel-delete]");
    if (fil) deleteHours(parseInt(fil.dataset.id));
  });
});
