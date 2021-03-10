import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal

class causal_prob(object):
    def __init__(self, **kwargs):
        None

    def is_pos_definite(self,x):
        eig_vals=np.linalg.eigvals(x)
        return np.all(eig_vals > 0)
    def get_small_pieces(self, idx):
        mu = self.mean[idx]
        mu_h = mu[0:2]
        mu_f = mu[2:]
        cov = self.cov[idx]
        cov_hh = cov[0:2, 0:2]
        cov_fh = cov[2:, 0:2]
        cov_hf = cov[0:2, 2:]
        cov_ff = cov[2:, 2:]
        return mu_h, mu_f, cov_hh, cov_fh, cov_hf, cov_ff
    def conditioned_mu(self, x_h):
        erg = {new_list: [] for new_list in range(0, len(self.mean))}
        for wlt in erg:
            mu_h, mu_f, cov_hh, cov_fh, cov_hf, cov_ff=self.get_small_pieces(wlt)
            dif_vec=x_h-mu_h
            added_mu_A=np.matmul(cov_fh,np.linalg.inv(cov_hh))
            added_mu=np.matmul(added_mu_A, dif_vec)
            erg[wlt]=mu_f+added_mu
        return erg
    def conditioning(self, vel):
        self.df=self.df.loc[self.df["ye"]>0]
        self.sub_df = [self.df.loc[self.df['idx'] == qrt].drop('idx', axis=1) for qrt in range(0, len(vel))]
        self.mean = [np.array(self.sub_df[qrt].mean()) for qrt in range(0, len(self.sub_df))]
        self.cov = [np.array(self.sub_df[qrt].cov()) for qrt in range(0, len(self.sub_df))]
        self.pi = [vel[qrt]['pi'] for qrt in vel]
    def conditioned_Sigma(self):
        erg = {new_list: [] for new_list in range(0, len(self.mean))}
        for wlt in erg:
            mu_h, mu_f, cov_hh, cov_fh, cov_hf, cov_ff=self.get_small_pieces(wlt)
            a=np.matmul(cov_fh, np.linalg.inv(cov_hh))
            second_mat=np.matmul(a, cov_hf)
            erg[wlt]=cov_ff-second_mat
        return erg

    def predict(self, xh, vel):
        new_mu = self.conditioned_mu(xh)
        print(new_mu)
        new_sigma = self.conditioned_Sigma()
        print(new_sigma)
        new_pi = self.conditioned_pi(vel, xh)
        print(new_pi)
    def conditioned_pi(self, vel, x_h):
        all_val=[]
        for wlt in vel:
            mu_h, mu_f, cov_hh, cov_fh, cov_hf, cov_ff = self.get_small_pieces(wlt)
            all_val.append(vel[wlt]['pi']*multivariate_normal(mean=mu_h, cov=cov_hh).pdf(x_h))
        erg = {nl: all_val[nl]/np.sum(all_val) for nl in range(0, len(self.mean))}
        return erg
    def get_dataset(self, params, start_pos,vel):

        xs, ys = np.random.multivariate_normal(start_pos['mu'], start_pos['Sigma'], params['N']).T
        idx=np.random.choice(len(vel), params['N'], p=[vel[rqt]['pi'] for rqt in vel])
        xe, ye=np.zeros((len(xs),)), np.zeros((len(ys),))
        for ix, qrt in enumerate(idx):
            vx, vy = np.random.multivariate_normal(vel[qrt]['mu'], vel[qrt]['Sigma'])
            xe[ix], ye[ix]=xs[ix]+vx, ys[ix]+vy
        d = {'idx': idx, 'xs': xs, 'ys': ys, 'xe': xe, 'ye': ye}
        self.df = pd.DataFrame(data=d)
        self.sub_df=[self.df.loc[self.df['idx'] == qrt].drop('idx', axis=1) for qrt in range(0, len(vel))]
        self.mean=[np.array(self.sub_df[qrt].mean()) for qrt in range(0, len(self.sub_df))]
        self.cov=[np.array(self.sub_df[qrt].cov()) for qrt in range(0, len(self.sub_df))]
        self.pi=[vel[qrt]['pi'] for qrt in vel]
    def plot_the_scene(self):
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.scatter(self.df['xs'], self.df['ys'], label='initial position', color='black')
        sel_col=['blue', 'green', 'red', 'cyan', 'orange', 'yellow']
        [ax.scatter(qrt['xe'], qrt['ye'], label=str(idx), color=sel_col[idx]) for idx, qrt in enumerate(self.sub_df)]
        ax.legend()
        plt.grid()
        plt.show()
    def do_xe_ye(self, params, do_prob, vel):
        new_xe, new_ye = np.random.multivariate_normal(do_prob['mu'], do_prob['Sigma'], params['N']).T
        self.df["xe"] = new_xe
        self.df["ye"] = new_ye
        #self.df["idx"] = 0
        self.sub_df = [self.df.loc[self.df['idx'] == qrt].drop('idx', axis=1) for qrt in range(0, len(vel))]
        self.mean = [np.array(self.sub_df[qrt].mean()) for qrt in range(0, len(self.sub_df))]
        self.cov = [np.array(self.sub_df[qrt].cov()) for qrt in range(0, len(self.sub_df))]
        self.pi = [vel[qrt]['pi'] for qrt in vel]

    def mahalabonis_dist(self, x, mu, Sigma):
        return -0.5*np.transpose(x-mu)*np.linalg.inv(Sigma)*(x-mu)
    def multivariate_gaussian_distribution(self, x, mu, Sigma):
        factor_A=1/np.sqrt((2*np.pi)**2*np.linalg.det(Sigma))
        factor_B=np.exp(self.mahalabonis_dist(x, mu, Sigma))
        erg=factor_A*factor_B
        return erg[0]
    def contour_plot(self):
        NGRID = 40
        X = np.linspace(-11, 11, NGRID)
        Y = np.linspace(-11, 11, NGRID)
        X, Y = np.meshgrid(X, Y)
        fig = plt.figure()
        ax = fig.add_subplot()
        Z = np.zeros((np.size(X, 0), np.size(X, 1)))
        for idx_A in range(0, np.size(X, 0)):
            for idx_B in range(0, np.size(X, 1)):
                x = np.array([X[idx_A, idx_B], Y[idx_A, idx_B]])
                for qrt in range(0, len(self.mean)):
                    mu_h, mu_f, cov_hh, cov_fh, cov_hf, cov_ff = self.get_small_pieces(qrt)
                    new_val=self.pi[qrt]*multivariate_normal(mean=mu_f, cov=cov_ff).pdf(x)
                    Z[idx_A, idx_B] += new_val
        # self.ax.plot_surface(self.X, self.Y, Z,  cmap='viridis',
        #               linewidth=0, antialiased=False, alpha=.3)
        ax.contour(X, Y, Z, 10, lw=3, cmap="autumn_r", linestyles="solid", offset=0)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.grid()
        plt.show()

if __name__ == '__main__':
    start_pos={'mu': np.array([0, 0]), 'Sigma': np.array([[.4, 0], [0, .4]])}
    vel={0: {'pi':.6, 'mu': np.array([8, 8]), 'Sigma': np.array([[1, 0.5], [0.5, 1]])},
         1:{'pi':.3, 'mu': np.array([-8, 2]), 'Sigma': np.array([[.4, -0.6], [-0.6, .4]])},
         2: {'pi': .1, 'mu': np.array([1, -7]), 'Sigma': np.array([[.4, -0.6], [-0.6, .4]])}
         }

    params={'N': 600}
    xh=np.array([5, 5])
    obj_causal = causal_prob()
    obj_causal.get_dataset(params, start_pos,vel)
    obj_causal.do_xe_ye(params, {'mu': np.array([8, 0]), 'Sigma': np.array([[.4, 0], [0, .4]])})
    obj_causal.conditioning()
    xf_pred=obj_causal.predict(xh, vel)
    obj_causal.plot_the_scene()
    obj_causal.contour_plot()