require "jekyll-import"

cwd = Dir.getwd
files = Dir.entries(cwd + "/imports/")

for item in files do
  if item.end_with?("xml")
    JekyllImport::Importers::Blogger.run({
      "source"                => cwd + "/imports/" + item,
      "no-blogger-info"       => false,
      "replace-internal-link" => false,
    })
  end 
end
