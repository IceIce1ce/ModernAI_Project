import os

class WandbLogger:
    def __init__(self, opt):
        try:
            import wandb
        except ImportError:
            raise ImportError("To use the Weights and Biases Logger please install wandb. Run `pip install wandb` to install it.")
        self._wandb = wandb
        if self._wandb.run is None:
            self._wandb.init(project=opt['wandb']['project'], config=opt, dir='experiments')
        self.config = self._wandb.config
        if self.config.get('log_eval', None):
            self.eval_table = self._wandb.Table(columns=['esti_image', 'noisy_image', 'gt_image', 'psnr', 'ssim'])
        else:
            self.eval_table = None
        if self.config.get('log_infer', None):
            self.infer_table = self._wandb.Table(columns=['esti_image', 'noisy_image', 'gt_image'])
        else:
            self.infer_table = None

    def log_metrics(self, metrics, commit=True):
        self._wandb.log(metrics, commit=commit)

    def log_image(self, key_name, image_array):
        self._wandb.log({key_name: self._wandb.Image(image_array)})

    def log_images(self, key_name, list_images):
        self._wandb.log({key_name: [self._wandb.Image(img) for img in list_images]})

    def log_checkpoint(self, current_epoch, current_step):
        model_artifact = self._wandb.Artifact(self._wandb.run.id + "_model", type="model")
        gen_path = os.path.join(self.config.path['checkpoint'], 'I{}_E{}_gen.pth'.format(current_step, current_epoch))
        opt_path = os.path.join(self.config.path['checkpoint'], 'I{}_E{}_opt.pth'.format(current_step, current_epoch))
        model_artifact.add_file(gen_path)
        model_artifact.add_file(opt_path)
        self._wandb.log_artifact(model_artifact, aliases=["latest"])

    def log_eval_data(self, cond_img, gt_img, psnr=None, ssim=None):
        if psnr is not None and ssim is not None:
            self.eval_table.add_data(self._wandb.Image(cond_img), self._wandb.Image(gt_img), psnr, ssim)
        else:
            self.infer_table.add_data(self._wandb.Image(cond_img), self._wandb.Image(gt_img))

    def log_eval_table(self, commit=False):
        if self.eval_table:
            self._wandb.log({'eval_data': self.eval_table}, commit=commit)
        elif self.infer_table:
            self._wandb.log({'infer_data': self.infer_table}, commit=commit)