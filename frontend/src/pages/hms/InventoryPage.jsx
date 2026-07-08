import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import DataTable from "../../components/DataTable";
import StatCard from "../../components/StatCard";
import { inventoryApi } from "../../api/client";

export default function InventoryPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    inventoryApi.items().then((r) => setItems(r.data));
  }, []);

  const lowStock = items.filter((i) => i.is_low_stock).length;

  const columns = [
    { key: "sku", label: "SKU" },
    { key: "name", label: "Item" },
    { key: "category", label: "Category", render: (r) => r.category_name },
    { key: "stock", label: "Stock", render: (r) => r.total_stock },
    { key: "reorder", label: "Reorder At", render: (r) => r.reorder_level },
    { key: "status", label: "Status", render: (r) => r.is_low_stock ? <span className="status-pill urgent">Low Stock</span> : <span className="status-pill completed">OK</span> },
  ];

  return (
    <AppShell title="Inventory" subtitle="Hospital supplies & stock">
      <div className="stats-row compact">
        <StatCard label="Total Items" value={items.length} icon="inventory" />
        <StatCard label="Low Stock" value={lowStock} icon="alert" accent="critical" />
      </div>
      <section className="panel">
        <DataTable columns={columns} rows={items} emptyMessage="No inventory items." />
      </section>
    </AppShell>
  );
}
