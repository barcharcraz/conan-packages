#include <GLFW/glfw3.h>
#include <cstdlib>


int main(int argc, char** argv) {
    if(!glfwInit()) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}