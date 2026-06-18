export default function Layout({ sidebar, children }) {
  return (
    <div className="flex">
      {sidebar}
      <main className="flex-1 p-6 bg-gray-50 min-h-[calc(100vh-4rem)]">
        {children}
      </main>
    </div>
  );
}
