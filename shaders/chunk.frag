#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
uniform vec3 bg_color;
uniform float water_line;
uniform float day_light;
uniform vec3 player_pos;

in vec2 uv;
in float shading;
in vec3 frag_world_pos;

flat in int face_id;
flat in int voxel_id;

vec3 sample_block_color(vec2 face_uv) {
    int layer_count = max(textureSize(u_texture_array_0, 0).z, 1);
    int layer = voxel_id % layer_count;
    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, layer)).rgb;

    // Procedural textures for blocks not present in the original texture array.
    if (voxel_id == 8) { // cobblestone / pierre taillée
        vec3 stone = texture(u_texture_array_0, vec3(face_uv, min(4, layer_count - 1))).rgb;
        float grid = step(0.92, fract(face_uv.x * 8.0)) + step(0.92, fract(face_uv.y * 8.0));
        float noise = fract(sin(dot(face_uv * 96.0, vec2(12.9898, 78.233))) * 43758.5453);
        tex_col = stone * (0.75 + 0.2 * noise) + vec3(0.08) * min(grid, 1.0);
    } else if (voxel_id == 9) { // planks
        vec3 wood = texture(u_texture_array_0, vec3(face_uv, min(7, layer_count - 1))).rgb;
        float plank_lines = step(0.95, fract(face_uv.y * 6.0));
        float grain = 0.85 + 0.2 * sin(face_uv.x * 60.0);
        tex_col = wood * vec3(1.15, 0.95, 0.75) * grain - vec3(0.12) * plank_lines;
    } else if (voxel_id == 10) { // brick
        vec3 clay = texture(u_texture_array_0, vec3(face_uv, min(3, layer_count - 1))).rgb;
        vec2 brick_uv = vec2(face_uv.x * 10.0, face_uv.y * 5.0);
        brick_uv.x += step(0.5, fract(brick_uv.y * 0.5)) * 0.5;
        float mortar = step(0.94, fract(brick_uv.x)) + step(0.9, fract(brick_uv.y));
        tex_col = clay * vec3(1.2, 0.55, 0.45) - vec3(0.28) * min(mortar, 1.0);
    } else if (voxel_id == 11) { // clay
        vec3 dirt = texture(u_texture_array_0, vec3(face_uv, min(3, layer_count - 1))).rgb;
        float variation = 0.9 + 0.1 * sin((face_uv.x + face_uv.y) * 50.0);
        tex_col = dirt * vec3(0.85, 0.95, 1.2) * variation;
    } else if (voxel_id == 12) { // glowstone
        vec3 stone = texture(u_texture_array_0, vec3(face_uv, min(4, layer_count - 1))).rgb;
        float cells = step(0.82, fract(face_uv.x * 12.0)) + step(0.82, fract(face_uv.y * 12.0));
        tex_col = stone * vec3(1.25, 1.05, 0.55) + vec3(0.25, 0.17, 0.03) * min(cells, 1.0);
    }
    return tex_col;
}

void main() {
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 tex_col = sample_block_color(face_uv);
    tex_col = pow(tex_col, gamma);

    float player_dist = distance(frag_world_pos, player_pos);
    float player_light = exp(-0.035 * player_dist * player_dist);
    float emissive = voxel_id == 12 ? 0.75 : 0.0;
    float light_level = max(day_light, emissive + player_light * 0.65);
    tex_col *= shading * light_level;

    // underwater effect
    if (frag_world_pos.y < water_line) tex_col *= vec3(0.0, 0.3, 1.0);

    //fog
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));

    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4(tex_col, 1.0);
}
