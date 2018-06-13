#WGAN read me
files staring with combined_ are images for training and testing
_rpr have 88% of pixels removed
_ have random shapes added to the image
test_out/images files have WGAN outputs; compare outputs and targets(ground truth)
/tools are used for the pix2pix.py files
pix2pix.py does image inpainting using GAN with inputs of pairs of images (amputated, ground truth)
pix2pix.py_wgangp implements WGAN-GP
mse_calc.py calculates MSE
