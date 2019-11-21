from prometheus_client.core import GaugeMetricFamily
import prometheus_client as prom
import time
from vault_integration import Vault

class CustomVaultExporter:

    def __init__(self):
        pass

    def collect(self):
        vault = Vault()
        tokens_info = vault.get_key_data_from_vault()

        for token_info in tokens_info:
            gauge = GaugeMetricFamily(
                name="vault_token_expire_time",
                documentation="Collect time remaining to expire Vault service token",
                labels=['display_name']
            )

            gauge.add_metric(
                labels=[token_info.name],
                value=token_info.expiration_time
            )
            yield gauge

if __name__ == "__main__":
    custom_exporter = CustomVaultExporter()
    prom.REGISTRY.register(custom_exporter)
    prom.start_http_server(9121)

    while True:
        time.sleep(30)