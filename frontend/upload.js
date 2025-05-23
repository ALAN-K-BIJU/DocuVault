document.getElementById("uploadForm").onsubmit = async function (e) {
  e.preventDefault();
  const form = e.target;
  const file = form.file.files[0];
  const username = form.username.value;
  const comment = form.comment.value;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("username", username);
  formData.append("comment", comment);

  try {
    const res = await fetch("https://03e949e65c1646648982c8106a1b01cd.vfs.cloud9.us-east-1.amazonaws.com:5000/documents/upload", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Server Error (${res.status}): ${errorText}`);
    }

    const result = await res.json();
    alert("Uploaded! Version ID: " + result.version_id);
  } catch (err) {
    console.error("Upload failed:", err);
    alert("Upload failed: " + err.message);
  }
};
