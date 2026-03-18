#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
uniform vec3 bg_color;
uniform float water_line;
uniform float day_light;

in vec2 uv;
in float shading;
in vec3 frag_world_pos;

flat in int face_id;
flat in int voxel_id;


void main() {
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    int layer_count = max(textureSize(u_texture_array_0, 0).z, 1);
    int layer = voxel_id % layer_count;

    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, layer)).rgb;
    tex_col = pow(tex_col, gamma);

    float emissive = voxel_id == 12 ? 0.75 : 0.0;
    float light_level = max(day_light, emissive);
    tex_col *= shading * light_level;

    // underwater effect
    if (frag_world_pos.y < water_line) tex_col *= vec3(0.0, 0.3, 1.0);

    //fog
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));

    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4(tex_col, 1.0);
}
