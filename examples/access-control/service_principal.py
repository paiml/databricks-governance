# Create a Service Principal that has access to the GovernanceCatalog
# in Databricks.

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import Privilege, SecurableType, PermissionsChange
import time

CATALOG_NAME="GovernanceCatalog"

def create_service_principal_with_catalog_access():
    """Create a service principal and grant it access to a governance catalog."""
    
    # Initialize the Databricks workspace client
    workspace = WorkspaceClient()
    
    print(f"Connected to Databricks workspace")
    
    # Step 1: Create the service principal
    sp_display_name = f"governance-service-principal"
    
    try:
        service_principal = workspace.service_principals.create(
            display_name=sp_display_name,
            active=True
        )
        print(f"Created service principal: {sp_display_name} (ID: {service_principal.id})")
    except Exception as e:
        print(f"Failed to create service principal: {e}")
        return None
    
    # Step 2: Wait a moment for the service principal to propagate
    time.sleep(2)
    
    # Step 3: Grant permissions on the catalog
    try:
        # Grant USAGE and SELECT privileges on the catalog
        # You can adjust privileges based on your needs
        permission_change = PermissionsChange(
            principal=service_principal.application_id,
            add=[Privilege.USAGE, Privilege.SELECT]
        )
        
        # Grant USAGE and SELECT privileges on the catalog
        grant_result = workspace.grants.update(
            securable_type=SecurableType.CATALOG,
            full_name=CATALOG_NAME,
            changes=[permission_change]
        )
        print(f"Granted catalog access to service principal for catalog: {CATALOG_NAME}")
    except Exception as e:
        print(f"Failed to grant catalog permissions: {e}")
        return service_principal

    
    return service_principal

if __name__ == "__main__":
    print("Creating Service Principal with Governance Catalog Access\n")
    
    # Create the service principal
    sp = create_service_principal_with_catalog_access()
    
    if sp:
        print(f"\nSuccess! Service principal created and configured:")
        print(f"   Name: {sp.display_name}")
    else:
        print("\nFailed to create and configure service principal")