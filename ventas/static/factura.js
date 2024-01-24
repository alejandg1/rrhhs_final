// Variable de objetos
let d = document
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener("DOMContentLoaded", function(e) {
  // Declaracion de variables
  let $subtotal = d.getElementById("id_subtotal");
  let $total = d.getElementById("id_total");
  let $iva = d.getElementById("id_iva");
  let $detailBody = d.getElementById("detalle");
  let $product = d.getElementById("product");
  let $cantidad = d.getElementById("cantidad")
  let $btnAdd = d.getElementById("btnadd");
  let $form = d.getElementById("form-container"); let details = [];
  if (details_fac.length > 0) {
    details = details_fac.map((item) => {
      const {
        prod: product_name,
        product_id: product,
        nh,
        quant: quantity,
        subtotal: subtotal,
        price: price
      } = item;
      return {
        subtotal,
        product,
        nh,
        quantity,
        product_name,
        price
      };
    });
    present();
    totals();
  }
  // Declaracion de metodos
  // ---------- calcula el sobretiempo y lo añade al arreglo detailOvertime[] ----------
  const calculation = (product_id, product, cantidad, precio) => {
    const exist = details.find((item) => item.product_name == product);
    if (exist) {
      if (
        !confirm(
          `¿Este producto ya ha sido ingresado desea actualizar la a cantidad a: ${cantidad}?`
        )
      )
        return;
      details = details.filter((det) => det.product_name !== product);
    }
    let calculado = parseFloat((cantidad * precio).toFixed(2));
    details.push({
      product: product_id,
      product_name: product,
      price: precio,
      quantity: cantidad,
      subtotal: calculado
    });
    present();
    totals();
  };

  const reCalculation = (vh) => {
    detailOvertime= detailOvertime.map((item) => {
      let { idHour, description, factor, nh } = item
      let value = parseFloat((vh * factor * nh).toFixed(2))
      c({ idHour, description, factor, nh, value })
      return { idHour, description, factor, nh, value } 
    })
    present()
    totals()
  }
  // ------------------- actualiza el detalle del sobretiempo seleccionado -----------
  // ---------------  borra el sobretiempo dado el id en el arreglo detailOvertime[] ------------
  const deleteHours = (product) => {
    details = details.filter((item) => item.product_name !== product);
    present();
    totals();
  };
  // recorre el arreglo detailOvertime y renderiza el detalle del sobretiempo -----------
  function present() {
    let detalle = document.getElementById("detalle");
    detalle.innerHTML = "";
    details.forEach((item) => {
      detalle.innerHTML += `<tr>
            <td>${item.product_name}</td>
            <td>${item.quantity}</td>
            <td>${item.price} $</td>
            <td>💰${item.subtotal}</td>
            <td class="text-center ">
                <button rel="rel-delete" data-id="${item.product_name}" class="text-danger" data-bs-toggle="tooltip" data-bs-title="Eliminar registro"><i class="bi bi-x-circle-fill"></i></button>
            </td>
          </tr>`;
    });
  }
  // ----- Sumariza del arreglo detailOvertime[] y lo renderiza en la tabla de la pagina -----
  function totals() {
    const sumTotals = details.reduce((acum, item) => {
      return (acum + item.subtotal)
    }, 0);
    let iva = parseInt($iva.options[$iva.selectedIndex].innerText)
    let calculo = (sumTotals * (iva / 100)) + sumTotals
    $subtotal.value = sumTotals.toFixed(2);
    $total.value = calculo.toFixed(2);
  }
  // ------------- manejo del DOM -------------
  $iva.addEventListener("change", async (e) => {
    e.preventDefault()
    totals()
  });
  // ---------- envia los datos del sobretiempo al backend por ajax para grabarlo ----------
  $form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (parseFloat(d.getElementById("id_subtotal").value) > 0.0) {
      const formData = new FormData($form);
      formData.append("detail", JSON.stringify(details));
      const request = await fetchPost(location.pathname, formData);
      console.log(formData)
      if (!request.ok) return console.log(request.data);
      window.location = backUrl;
    } else {
      alert("!!!Ingrese productos para grabar!!!");
    }
  });
  // -------- registra las horas del sobretiempo en el arreglo detailOvertime[] ---------
  $btnAdd.addEventListener("click", (e) => {
    if (parseFloat($product.value) > 0.0 && parseInt($cantidad.value) > 0) {
      e.preventDefault()
      let nombre = $product.options[$product.selectedIndex].innerText
      let price = $product.options[$product.selectedIndex].dataset.value
      let id = $product.value
      calculation(
        id,
        nombre,
        parseInt($cantidad.value),
        parseFloat(price)
      );
      d.getElementById("id_subtotal").value = "";
    } else {
      alert(
        "Faltan datos de ingresar"
      );
    }
    totals()
  });
  //---- por delegacion de eventos seleccionada la fila de las horas del sobretiempo ----------
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener("click", (e) => {
    const fil = e.target.closest("button[rel=rel-delete]");
    if (fil) deleteHours(fil.dataset.id);
  });
});
