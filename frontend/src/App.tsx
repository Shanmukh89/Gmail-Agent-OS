import { useState, useEffect } from 'react';
import { 
  Inbox, 
  Bell, 
  BellOff,
  Tags,
  Plus,
  Trash2,
  TerminalSquare
} from 'lucide-react';

// No hardcoded initial categories needed, will fetch from API
interface Category {
  id: number;
  name: string;
  description: string;
  notify: boolean;
}

function App() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);
  
  // New category form state
  const [newCatName, setNewCatName] = useState('');
  const [newCatDesc, setNewCatDesc] = useState('');
  const [newCatNotify, setNewCatNotify] = useState(false);

  const API_URL = 'http://127.0.0.1:8000';

  const fetchCategories = async () => {
    try {
      const res = await fetch(`${API_URL}/categories/`);
      if (res.ok) {
        const data = await res.json();
        setCategories(data);
      }
    } catch (e) {
      console.error("Failed to fetch categories", e);
    }
  };

  useEffect(() => {
    fetchCategories().then(() => setIsLoaded(true));
  }, []);

  const toggleNotify = async (cat: Category) => {
    try {
      const updatedCat = { ...cat, notify: !cat.notify };
      const res = await fetch(`${API_URL}/categories/${cat.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedCat)
      });
      if (res.ok) {
        setCategories(cats => cats.map(c => c.id === cat.id ? updatedCat : c));
      }
    } catch (e) {
      console.error("Failed to update notification status", e);
    }
  };

  const deleteCategory = async (id: number) => {
    try {
      const res = await fetch(`${API_URL}/categories/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setCategories(cats => cats.filter(c => c.id !== id));
      }
    } catch (e) {
      console.error("Failed to delete category", e);
    }
  };

  const handleAddCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCatName.trim()) return;

    try {
      const payload = {
        name: newCatName,
        description: newCatDesc,
        notify: newCatNotify
      };
      
      const res = await fetch(`${API_URL}/categories/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        const data = await res.json();
        setCategories([...categories, data]);
        setNewCatName('');
        setNewCatDesc('');
        setNewCatNotify(false);
      }
    } catch (e) {
      console.error("Failed to add category", e);
    }
  };

  const [isSyncing, setIsSyncing] = useState(false);

  const triggerSync = async () => {
    setIsSyncing(true);
    try {
      const res = await fetch(`${API_URL}/sync/`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        alert(`Sync complete! Processed ${data.processed} emails. Notifications fired: ${data.notifications_fired}`);
      } else {
        const err = await res.json();
        alert(`Sync failed: ${err.detail || 'Unknown error'}`);
      }
    } catch (e) {
      console.error("Failed to sync", e);
      alert("Failed to reach backend sync endpoint.");
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div className="min-h-screen flex text-neutral-200 selection:bg-neutral-800 selection:text-white">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-y-0 border-l-0 flex flex-col p-6 sticky top-0 h-screen">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-8 h-8 flex items-center justify-center border border-neutral-700 bg-neutral-900 rounded">
            <TerminalSquare className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-xl font-semibold tracking-tight text-white">
            MailMind
          </h1>
        </div>

        <nav className="flex-1 space-y-1">
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded transition-colors duration-150 text-sm bg-neutral-800 text-white font-medium">
            <Tags className="w-4 h-4" />
            <span>Routing Rules</span>
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className={`flex-1 p-8 transition-opacity duration-300 max-w-4xl ${isLoaded ? 'opacity-100' : 'opacity-0'}`}>
        <header className="mb-10 flex justify-between items-end">
          <div>
            <h2 className="text-2xl font-semibold tracking-tight text-white">Routing Rules</h2>
            <p className="text-neutral-500 text-sm mt-1">Configure your AI categories and notification triggers.</p>
          </div>
          <button 
            onClick={triggerSync}
            disabled={isSyncing}
            className="bg-neutral-800 hover:bg-neutral-700 border border-neutral-700 text-white px-4 py-2 rounded text-sm font-medium flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <Inbox className={`w-4 h-4 ${isSyncing ? 'animate-pulse' : ''}`} /> 
            {isSyncing ? 'Running Sync...' : 'Run Sync Now'}
          </button>
        </header>

        <div className="space-y-8">
          {/* Add Category Form */}
          <div className="glass-card p-6 rounded border border-neutral-800">
            <h3 className="text-sm font-medium text-neutral-300 mb-4 uppercase tracking-wider">Add New Rule</h3>
            <form onSubmit={handleAddCategory} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs text-neutral-500">Category Name</label>
                  <input 
                    type="text" 
                    value={newCatName}
                    onChange={(e) => setNewCatName(e.target.value)}
                    placeholder="e.g. Invoices" 
                    className="w-full bg-neutral-900 border border-neutral-700 rounded px-3 py-2 text-sm text-neutral-200 focus:outline-none focus:border-neutral-500"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs text-neutral-500">LLM Prompt Description</label>
                  <input 
                    type="text" 
                    value={newCatDesc}
                    onChange={(e) => setNewCatDesc(e.target.value)}
                    placeholder="e.g. Receipts, bills, and financial docs" 
                    className="w-full bg-neutral-900 border border-neutral-700 rounded px-3 py-2 text-sm text-neutral-200 focus:outline-none focus:border-neutral-500"
                  />
                </div>
              </div>
              <div className="flex items-center justify-between pt-2">
                <label className="flex items-center gap-2 cursor-pointer group">
                  <input 
                    type="checkbox" 
                    checked={newCatNotify}
                    onChange={(e) => setNewCatNotify(e.target.checked)}
                    className="hidden"
                  />
                  <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${newCatNotify ? 'bg-green-500 border-green-500' : 'border-neutral-600 group-hover:border-neutral-500'}`}>
                    {newCatNotify && <Bell className="w-3 h-3 text-black" />}
                  </div>
                  <span className="text-sm text-neutral-400 group-hover:text-neutral-300">Trigger Notification</span>
                </label>
                <button 
                  type="submit"
                  disabled={!newCatName.trim()}
                  className="bg-white text-black px-4 py-2 rounded text-sm font-medium flex items-center gap-2 hover:bg-neutral-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Plus className="w-4 h-4" /> Add Rule
                </button>
              </div>
            </form>
          </div>

          {/* Active Categories List */}
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wider">Active Rules ({categories.length})</h3>
            <div className="space-y-3">
              {categories.map(cat => (
                <div key={cat.id} className="glass-card flex items-center justify-between p-4 rounded group hover:border-neutral-600 transition-colors">
                  <div className="flex-1 min-w-0 pr-4">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-white">{cat.name}</span>
                    </div>
                    <p className="text-sm text-neutral-500 truncate">{cat.description || 'No description provided.'}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <button 
                      onClick={() => toggleNotify(cat.id)}
                      className="p-2 rounded hover:bg-neutral-800 transition-colors"
                      title={cat.notify ? "Notifications ON" : "Notifications OFF"}
                    >
                      {cat.notify ? (
                        <Bell className="w-5 h-5 text-green-500" />
                      ) : (
                        <BellOff className="w-5 h-5 text-neutral-600" />
                      )}
                    </button>
                    <button 
                      onClick={() => deleteCategory(cat.id)}
                      className="p-2 rounded text-neutral-600 hover:text-red-400 hover:bg-red-400/10 transition-colors opacity-0 group-hover:opacity-100"
                      title="Delete Rule"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
              
              {categories.length === 0 && (
                <div className="text-center py-12 border border-dashed border-neutral-800 rounded">
                  <Tags className="w-8 h-8 text-neutral-700 mx-auto mb-3" />
                  <p className="text-neutral-500 text-sm">No routing rules defined.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
