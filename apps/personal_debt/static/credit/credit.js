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
  // let $btnGrabar = d.getElementById("btnGrabar");
  let $form = d.getElementById("form-container");
  let detailCredit = [];
  if (detail.length > 0) {
    detailCredit = detail.map((item) => {
      const { id: det_id, quot: quote, st: status, bal: balance } = item;
      return { det_id, quote, status, balance };
    });
    present();
  }

  // Declaracion de metodos
  function present() {
    print(detailCredit);
    c("estoy en present()");
    let detalle = document.getElementById("detalle");
    detalle.innerHTML = "";
    detailCredit.forEach((detail) => {
      detalle.innerHTML += `<tr>
            <td>${detail.quote}</td>
            <td>${detail.status}</td>
            <td>${detail.balance}</td>
            <td>

            </tr>`;
    });
  }

  $btnadd.addEventListener("click", (e) => {
    e.preventDefault();
    let date = $date_discount.value;
    let quota = $nquota.value;
    let status = $status.value;
    let balance = $balance.value;
    detailCredit.push({ date, quota, status, balance });
    present();
  });

  $form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData($form);
    formData.append("detail", JSON.stringify(detailCredit));
    const request = await fetchPost(location.pathname, formData);
    console.log(formData);
    if (!request.ok) return c(request);
    window.location = backUrl;
  });

  const deleteHours = (id) => {
    detailCredit = detailCredit.filter((item) => item.id !== id);
    present();
  };
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener("click", (e) => {
    const fil = e.target.closest("button[rel=rel-delete]");
    if (fil) deleteHours(parseInt(fil.dataset.id));
  });
});
