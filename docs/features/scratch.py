from google.cloud import aiplatform_v1beta1
import inspect

print("--- Inspecting google.cloud.aiplatform_v1beta1.services ---")
if hasattr(aiplatform_v1beta1, 'services'):
    for name, obj in inspect.getmembers(aiplatform_v1beta1.services):
        if inspect.ismodule(obj):
            print(f"  Module in services: {name}")
            # Optionally, inspect members of this submodule if it seems relevant
            # for sub_name, sub_obj in inspect.getmembers(obj):
            #     if inspect.isclass(sub_obj) and sub_name.endswith("Client"):
            #         print(f"    Client Class in services.{name}: {sub_name}")
        if inspect.isclass(obj) and name.endswith("Client"):
            print(f"  Client Class directly in services: {name}")
else:
    print("  google.cloud.aiplatform_v1beta1.services does not exist or has no members to inspect directly.")

print("\n--- Inspecting google.cloud.aiplatform_v1beta1 directly ---")
for name, obj in inspect.getmembers(aiplatform_v1beta1):
    if inspect.isclass(obj) and name.endswith("Client"):
        print(f"  Client Class in aiplatform_v1beta1: {name}")

# Specific check for PromptRegistryServiceClient if the above doesn't find it
try:
    from google.cloud.aiplatform_v1beta1.services.prompt_registry_service import PromptRegistryServiceClient
    print("\nSUCCESS: Found PromptRegistryServiceClient at google.cloud.aiplatform_v1beta1.services.prompt_registry_service.PromptRegistryServiceClient")
except ImportError:
    print("\nFAILED: Could not import PromptRegistryServiceClient from ...services.prompt_registry_service")

try:
    from google.cloud.aiplatform_v1beta1 import PromptRegistryServiceClient
    print("\nSUCCESS: Found PromptRegistryServiceClient at google.cloud.aiplatform_v1beta1.PromptRegistryServiceClient")
except ImportError:
    print("\nFAILED: Could not import PromptRegistryServiceClient from ...aiplatform_v1beta1")

try:
    from google.cloud.aiplatform.gapic.services.prompt_registry_service import PromptRegistryServiceClient
    print("\nSUCCESS: Found PromptRegistryServiceClient at google.cloud.aiplatform.gapic.services.prompt_registry_service.PromptRegistryServiceClient")
except ImportError:
    print("\nFAILED: Could not import PromptRegistryServiceClient from ...aiplatform.gapic.services.prompt_registry_service")
except AttributeError: # If 'gapic' itself is not an attribute
    print("\nFAILED: google.cloud.aiplatform.gapic does not exist or no services sub-attribute.")


