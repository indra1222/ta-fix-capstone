// ======================================================================
//  SILENT NOTIFICATION SYSTEM (ALL NOTIFICATIONS DISABLED)
//  - Tidak menampilkan UI notifikasi
//  - Semua notifikasi dibungkam (success, error, warning, info)
//  - confirm() langsung otomatis YES
//  - NotificationContainer tetap ada (dummy) agar tidak error di App.js
// ======================================================================

// GLOBAL NotificationManager (Silent)
export const NotificationManager = {
  // Generic handler
  show: (config = {}) => {
    const id = Date.now() + Math.random();

    // Auto-confirm behavior
    if (config.type === "confirm" && typeof config.onConfirm === "function") {
      config.onConfirm(); // langsung lanjut tanpa popup
    }

    return id; // return fake ID supaya aman
  },

  remove: () => {},
  subscribe: () => () => {},

  // Shortcut methods (dibungkam)
  success: () => {},
  error: () => {},
  warning: () => {},
  info: () => {},

  confirm: (title, message, onConfirm) => {
    if (typeof onConfirm === "function") onConfirm(); // auto-YES
    return Date.now();
  }
};

// Dummy Notification Container
// Tetap diexport agar <NotificationContainer /> tidak menyebabkan error
export const NotificationContainer = () => null;

// Default export
export default NotificationContainer;
