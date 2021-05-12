#!/usr/bin/env python3
from aws_cdk import core
from stacks.vpc_stack import VpcStack
from stacks.bastion_stack import BastionStack
from stacks.security_stack import SecurityStack
from stacks.alb_stack import AlbStack
from stacks.rds_stack import RdsStack

app = core.App()

dev_stage = app.node.try_get_context("dev")

vpc_stack = VpcStack(app,
                     "vpc",
                     env=core.Environment(account=dev_stage['account_id'],
                                          region="ap-northeast-2"),
                     stage=dev_stage)
security_stack = SecurityStack(app,
                               "sg",
                               env=core.Environment(
                                   account=dev_stage['account_id'],
                                   region="ap-northeast-2"),
                               vpc=vpc_stack.vpc,
                               stage=dev_stage)
bastion_stack = BastionStack(app,
                             "bastion",
                             env=core.Environment(
                                 account=dev_stage['account_id'],
                                 region="ap-northeast-2"),
                             vpc=vpc_stack.vpc,
                             sg=security_stack.bastion_sg,
                             stage=dev_stage)
alb_stack = AlbStack(app,
                     "alb",
                     env=core.Environment(account=dev_stage['account_id'],
                                          region="ap-northeast-2"),
                     vpc=vpc_stack.vpc,
                     sg=security_stack.alb_sg,
                     stage=dev_stage)
rds_stack = RdsStack(app,
                     "rds",
                     env=core.Environment(account=dev_stage['account_id'],
                                          region="ap-northeast-2"),
                     vpc=vpc_stack.vpc,
                     asg_sg=alb_stack.asg_sg,
                     stage=dev_stage)

app.synth()
