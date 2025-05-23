async function fetchVersions() {
  const filename = document.getElementById("versionFile").value;

  try {
    const res = await fetch(`https://03e949e65c1646648982c8106a1b01cd.vfs.cloud9.us-east-1.amazonaws.com:5000/documents/versions/${filename}`);

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Server Error (${res.status}): ${errorText}`);
    }

    const versions = await res.json();
    const list = document.getElementById("versionList");
    list.innerHTML = "";

    versions.forEach(v => {
      const item = document.createElement("li");
      item.textContent = `Version: ${v.VersionId}, Latest: ${v.IsLatest}, Time: ${v.LastModified}`;
      list.appendChild(item);
    });

  } catch (err) {
    console.error("Failed to fetch versions:", err);
    alert("Failed to fetch versions: " + err.message);
  }
}
