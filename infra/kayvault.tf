data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                = "${var.app_name}-kv-${substr(md5(azurerm_resource_group.main.id), 0, 8)}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  enable_rbac_authorization   = true
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false  # false pour pouvoir supprimer en dev
}