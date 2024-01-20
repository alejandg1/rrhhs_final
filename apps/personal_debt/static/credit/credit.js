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

  $form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData($form);
    formData.append("detail", JSON.stringify(detailCredit));
    const request = await fetchPost(location.pathname, formData);
    if (!request.ok) return c(request);
    window.location = backUrl;
  });

  const deleteHours = (id) => {
    detailCredit = detailCredit.filter((item) => item.idHour !== id);
    present();
    totals();
  };
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener("click", (e) => {
    const fil = e.target.closest("button[rel=rel-delete]");
    if (fil) deleteHours(parseInt(fil.dataset.id));
  });
});
