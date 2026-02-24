resource "azurerm_container_registry" "main" {
  name                = "${var.app_name}registry"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false   # sécurité : admin désactivé
}