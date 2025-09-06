import React from 'react'

const Tabs = React.forwardRef(({ className = '', ...props }, ref) => (
  <div ref={ref} className={className} {...props} />
))
Tabs.displayName = 'Tabs'

const TabsList = React.forwardRef(({ className = '', ...props }, ref) => (
  <div
    ref={ref}
    className={`inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground ${className}`}
    {...props}
  />
))
TabsList.displayName = 'TabsList'

const TabsTrigger = React.forwardRef(({ className = '', value, ...props }, ref) => {
  const [activeTab, setActiveTab] = React.useState(null)
  
  return (
    <button
      ref={ref}
      className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm ${className}`}
      onClick={() => {
        const tabsContent = document.querySelectorAll('[data-tab-content]')
        tabsContent.forEach(content => {
          content.style.display = content.getAttribute('data-tab-content') === value ? 'block' : 'none'
        })
        
        const triggers = document.querySelectorAll('[data-tab-trigger]')
        triggers.forEach(trigger => {
          trigger.setAttribute('data-state', trigger.getAttribute('data-tab-trigger') === value ? 'active' : 'inactive')
        })
      }}
      data-tab-trigger={value}
      {...props}
    />
  )
})
TabsTrigger.displayName = 'TabsTrigger'

const TabsContent = React.forwardRef(({ className = '', value, ...props }, ref) => (
  <div
    ref={ref}
    className={`mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${className}`}
    data-tab-content={value}
    {...props}
  />
))
TabsContent.displayName = 'TabsContent'

export { Tabs, TabsList, TabsTrigger, TabsContent }