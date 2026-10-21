// Event specification: every parameter each GTM tag reads, with its type.
// Mirrors the specification in the project README.
module.exports = {
  resume_download: { file_name: 'string', link_location: 'string' },
  project_click: { project_name: 'string', project_slug: 'string', link_location: 'string' },
  contact_click: { contact_method: 'string', link_location: 'string' },
  outbound_click: { link_domain: 'string', link_url: 'string', link_location: 'string' },
  scroll_depth: { depth_percent: 'number' },
};

module.exports.LINK_LOCATIONS = [
  'landing_card', 'projects_index', 'landing_button', 'navbar', 'footer', 'page_body',
];
module.exports.CONTACT_METHODS = ['email', 'linkedin', 'github'];
