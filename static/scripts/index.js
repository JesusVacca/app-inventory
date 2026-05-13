document.addEventListener('DOMContentLoaded', () => {
  const ACTIVE_INDEX_KEY = 'menuActiveIndex';
  const OPEN_DROPDOWN_KEY = 'openDropdownKey';
  const toasts = document.querySelector('div.toasts');
  const message = document.querySelector('.page__header__message');
  const hiddenMessage = localStorage.getItem('hiddenMessage');

  const buttonLogout = document.querySelector('li.logout a');

  buttonLogout.addEventListener('click',()=>{
      const dataUrl = buttonLogout.getAttribute('data-url');
      Swal.fire({
        icon:'info',
        title: "¿Esta seguro que desea cerrar sesión?",
        showCancelButton: true,
        confirmButtonText: "Si",
        cancelButtonText:"No, cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = dataUrl;
          localStorage.removeItem('hiddenMessage');
        }
      });
  })

  if(!hiddenMessage){
    message.innerHTML = 'Hola, ¡Bienvenido!';
    setTimeout(()=>{
      message.innerHTML = '';
      localStorage.setItem('hiddenMessage',true);
    },5000);
  }


  if(toasts){
    let timer = 5000;
      toasts.querySelectorAll('.toast').forEach((toast, i)=>{
        const delay = i * .4;
        timer += delay * 500;
        setTimeout(()=>{
          toast.classList.add('show')
          toast.style.setProperty('--delay',`${delay}s`);
        },delay * 500)
      })
      setTimeout(()=>{
        toasts.querySelectorAll('.toast').forEach((toast, i)=>{
          toast.style.opacity = '0.8';
        })
      },timer)
  }


  // Lista de dropdown parents (para generar/usar keys estables)
  const dropdownParents = Array.from(document.querySelectorAll('.menu__item--dropdown'));

  // Asegura data-menu-key para cada dropdown parent (determinístico por su índice entre dropdowns)
  dropdownParents.forEach((parent, i) => {
    if (!parent.dataset.menuKey) {
      // preferimos id si existe, si no usamos un key generado estable por índice
      parent.dataset.menuKey = parent.id ? parent.id : `menu-dropdown-${i}`;
    }
  });

  // Lista plana y en orden DOM de todos los "elementos activables" del menú:
  // - botones/links top-level con clase .menu__link (incluye los toggles que son botones)
  // - links dentro de dropdowns (.dropdown__link)
  const items = Array.from(document.querySelectorAll('.menu .menu__link, .dropdown__menu .dropdown__link'));

  // utilidades
  const closeAllDropdowns = () => {
    dropdownParents.forEach(p => {
      p.classList.remove('open');
      p.querySelector('.dropdown__menu')?.classList.remove('open');
      p.querySelector('.dropdown__toggle')?.classList.remove('active');
    });
  };
  const removeActiveFromAll = () => {
    items.forEach(it => it.classList.remove('active'));
    document.querySelectorAll('.dropdown__toggle.active').forEach(btn => btn.classList.remove('active'));
  };
  const removeActiveFromDropdownsOnly = () => {
    document.querySelectorAll('.menu__item--dropdown .dropdown__toggle.active, .menu__item--dropdown .dropdown__menu .dropdown__link.active')
      .forEach(el => el.classList.remove('active'));
  };

  /* -----------------------
     Restaurar dropdown abierto (si existe)
     ----------------------- */
  const savedOpenKey = localStorage.getItem(OPEN_DROPDOWN_KEY);
  if (savedOpenKey) {
    const parent = document.querySelector(`.menu__item--dropdown[data-menu-key="${savedOpenKey}"]`);
    if (parent) {
      // abrir solo ese
      closeAllDropdowns();
      parent.classList.add('open');
      parent.querySelector('.dropdown__menu')?.classList.add('open');
      parent.querySelector('.dropdown__toggle')?.classList.add('active');
    } else {
      localStorage.removeItem(OPEN_DROPDOWN_KEY);
    }
  }

  /* -----------------------
     Restaurar elemento activo por índice (si existe)
     ----------------------- */
  const savedIndex = localStorage.getItem(ACTIVE_INDEX_KEY);
  if (savedIndex !== null) {
    const idx = parseInt(savedIndex, 10);
    if (!Number.isNaN(idx) && idx >= 0 && idx < items.length) {
      removeActiveFromAll();
      const el = items[idx];
      el.classList.add('active');

      // si este elemento está dentro de un dropdown, abrir ese dropdown y guardar open key
      const parent = el.closest('.menu__item--dropdown');
      if (parent) {
        closeAllDropdowns();
        parent.classList.add('open');
        parent.querySelector('.dropdown__menu')?.classList.add('open');
        parent.querySelector('.dropdown__toggle')?.classList.add('active');
        localStorage.setItem(OPEN_DROPDOWN_KEY, parent.dataset.menuKey);
      } else {
        // si es un link top-level, asegurarnos de no tener dropdown persistente abierto
        // (si quieres mantener el dropdown abierto aunque el top-link esté activo, comenta la línea siguiente)
        // localStorage.removeItem(OPEN_DROPDOWN_KEY);
      }
    } else {
      // índice inválido -> limpiar
      localStorage.removeItem(ACTIVE_INDEX_KEY);
    }
  }

  /* -----------------------
     Click listeners para cada item (guarda índice)
     ----------------------- */
  items.forEach((el, index) => {
    el.addEventListener('click', (ev) => {
      // Detectar si es el toggle del dropdown (botón)
      const isToggle = el.classList.contains('dropdown__toggle') || el.matches('button.dropdown__toggle');
      const parent = el.closest('.menu__item--dropdown');

      // siempre quitar active de todo (solo 1 activo)
      removeActiveFromAll();

      if (isToggle && parent) {
        // Toggle de dropdown
        const willOpen = !parent.classList.contains('open');

        // cerrar otros y abrir/activar el actual
        closeAllDropdowns();
        if (willOpen) {
          parent.classList.add('open');
          parent.querySelector('.dropdown__menu')?.classList.add('open');
          el.classList.add('active');
          // guardar índice y dropdown key
          localStorage.setItem(ACTIVE_INDEX_KEY, index);
          localStorage.setItem(OPEN_DROPDOWN_KEY, parent.dataset.menuKey);
        } else {
          parent.classList.remove('open');
          parent.querySelector('.dropdown__menu')?.classList.remove('open');
          el.classList.remove('active');
          localStorage.removeItem(ACTIVE_INDEX_KEY);
          localStorage.removeItem(OPEN_DROPDOWN_KEY);
        }

        // evitar comportamiento por defecto de botón y que el event burbujee
        ev.preventDefault();
        ev.stopPropagation();
        return;
      }

      // Si es link normal (top-level o dentro de dropdown)
      el.classList.add('active');
      // Guardar índice
      localStorage.setItem(ACTIVE_INDEX_KEY, index);

      if (parent) {
        // si es un link dentro de dropdown -> abrir su parent y persistirlo
        closeAllDropdowns();
        parent.classList.add('open');
        parent.querySelector('.dropdown__menu')?.classList.add('open');
        parent.querySelector('.dropdown__toggle')?.classList.add('active');
        localStorage.setItem(OPEN_DROPDOWN_KEY, parent.dataset.menuKey);
      } else {
        // link top-level -> cerrar dropdowns
        closeAllDropdowns();
        localStorage.removeItem(OPEN_DROPDOWN_KEY);
      }

      // no preventDefault: si es <a> navegará y la persistencia queda guardada previamente
    });
  });

  /* -----------------------
     Cerrar dropdowns y quitar active de dropdowns al click fuera
     ----------------------- */
  document.addEventListener('click', (ev) => {
    // Si el click ocurrió dentro del sidebar/menu, pero no dentro de un dropdown abierto, igual cerramos.
    // Solo evitamos cerrar cuando el click está dentro del dropdown que ya está abierto (para no interferir).
    const clickedInsideOpenDropdown = !!ev.target.closest('.menu__item--dropdown.open');
    if (clickedInsideOpenDropdown) return;

    // cerrar y quitar active solo de dropdowns (no tocamos links top-level que estén activos)
    closeAllDropdowns();
    removeActiveFromDropdownsOnly();
    localStorage.removeItem(OPEN_DROPDOWN_KEY);
  });

  /* -----------------------
     Cerrar si se presiona Escape
     ----------------------- */
  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape') {
      closeAllDropdowns();
      removeActiveFromDropdownsOnly();
      localStorage.removeItem(OPEN_DROPDOWN_KEY);
    }
  });
});
